from fastapi import FastAPI, Query,HTTPException
from azure.cosmos import CosmosClient
from dotenv import load_dotenv
import os
import re
import unicodedata
import inflect
import requests
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




load_dotenv()
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE")
COSMOS_CONTAINER_NUTRIENTS = os.getenv("COSMOS_CONTAINER_NUTRIENTS")
COSMOS_CONTAINER_COMPAT = os.getenv("COSMOS_CONTAINER_COMPAT")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
client_gemini=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
database = client.get_database_client(COSMOS_DATABASE)

container_macros= database.get_container_client(COSMOS_CONTAINER_NUTRIENTS)
container_compat = database.get_container_client(COSMOS_CONTAINER_COMPAT)

p = inflect.engine()

def normalizar(text: str):

    text = text.lower().strip()

    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")

    text = re.sub(r"[^\w\s]", "", text)

    singular = p.singular_noun(text)

    return singular if singular else text

@app.get("/")
def comprobacion():
    return print("API funcionando")



@app.get("/tipos")
def tipos(food):
    food_norm = normalizar(food)

    query = "SELECT c.id FROM c WHERE CONTAINS(c.id, @texto)"
    parameters = [{"name": "@texto", "value": food_norm}]

    items = list(container_compat.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if not items:
        return {"error": f"No se encontraron tipos de '{food}'"}



    resultados = []

    for item in items:
        nombre = item["id"].lower()

        palabras = set(nombre.split())


        if food_norm in palabras or nombre.endswith(food_norm) or nombre == food_norm:
            resultados.append(nombre)

    resultados = sorted(set(resultados))

    return {
        "tipos": resultados
    }

@app.get("/macros")
def macros(food):
    food_norm = normalizar(food)

    query = "SELECT * FROM c WHERE c.id = @id"
    parameters = [{"name": "@id", "value": food_norm}]

    items = list(container_macros.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if not items:
        return {"error": "Alimento no encontrado en la base de datos"}

    doc = items[0]

    return {
        "alimento": food,
        "macros": {
            "energia": doc.get("Energy") ,
            "proteinas": doc.get("Proteins"),
            "grasas": doc.get("Fat"),
            "carbohidratos": doc.get("Carbohydrate")
        }
    }

@app.get("/recomendar")
def recomendar(foods: list[str]=Query(...)):
        
    # 1) Normalizamos lo que manda el usuario
    foods_normalizados = []
    for f in foods:
        f = f.lower().strip()
        if f != "":
            foods_norm=normalizar(f)
            foods_normalizados.append(foods_norm)


    # 2) Si no hay ingredientes válidos, devolvemos error

    # 3) Para cada ingrediente, buscamos su documento en Cosmos
    #    y convertimos sus parejas en un diccionario tipo:
    #    {"garlic": 0.91, "basil": 0.88, ...}
    listas_parejas = []

    for food_id in foods_normalizados:
        query = "SELECT * FROM c WHERE c.id = @id"
        parameters = [{"name": "@id", "value": food_id}]

        items = list(container_compat.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        # Si no encuentra ese alimento en Cosmos, devolvemos error
        if len(items) == 0:
            raise HTTPException(
            status_code=404,
            detail=f'No se ha encontrado el alimento "{food_id}" en la base de datos.'
        )

        # Cogemos el primer documento encontrado
        doc = items[0]

        # Sacamos la lista de parejas del documento
        parejas = doc.get("parejas", [])

        # La convertimos en diccionario
        parejas_dict = {}

        for p in parejas:
            nombre_pareja = p["food"]
            score_pareja = p["score"]
            parejas_dict[nombre_pareja] = score_pareja

        # Guardamos ese diccionario en una lista general
        listas_parejas.append(parejas_dict)

    # 4) CASO 1: solo un ingrediente
    if len(foods_normalizados) == 1:
        resultado = []

        for food, score in listas_parejas[0].items():
            resultado.append({
                "food": food,
                "score": score
            })

        # Ordenamos por score de mayor a menor
        resultado.sort(key=lambda x: x["score"], reverse=True)

        return {
            "recomendaciones": resultado[:15]
        }
    
    contador_apariciones = Counter()
    suma_scores = Counter()

    for dic in listas_parejas:
        for food, score in dic.items():
            contador_apariciones[food] += 1
            suma_scores[food] += score

    # 6) Decidimos el mínimo de apariciones
    #    Si hay 2 ingredientes, pedimos que aparezca en los 2
    #    Si hay 3 o más, pedimos que aparezca al menos en n-1
    resultado=[]
    if len(foods_normalizados) == 2:
        min_apariciones = 2
    else:
        min_apariciones = len(foods_normalizados) - 1

    for food, apariciones in contador_apariciones.items():
        if apariciones >= min_apariciones:
            score_medio = suma_scores[food] / apariciones

            resultado.append({
                "food": food,
            })



    


    return {
        "recomendaciones": resultado[:15]
    }
  
        

def separar_recetas(texto: str):
    texto = texto.strip().strip('"')
    texto = texto.replace("\\n", "\n")

    bloques = texto.split("---")
    recetas = []

    for bloque in bloques:
        bloque = bloque.strip()

        if not bloque:
            continue

        partes = bloque.split("\n", 1)

        titulo = partes[0].replace("##", "").strip()
        cuerpo = partes[1].strip() if len(partes) > 1 else ""

        recetas.append({
            "titulo": titulo,
            "cuerpo": cuerpo

        })

    return recetas






@app.get("/recetas")
async def recetas(foods: list[str]=Query(...), recomendacion: list[str]=Query(...)):



    prompt=f"""
    Eres un chef creativo especializado en maridaje de ingredientes.

    Lista de alimentos dados por el usuario: {foods}

    Tarea:
    Genera recetas con la lista de alimentos base y con {recomendacion}. 
    Quiero recetas breves y realistas usando el alimento principal y
    {recomendacion}.

    Requisitos:
    - Devuelve solo recetas útiles.
    - Cada receta debe incluir:
    1. nombre
    2. ingredientes
    3. pasos
    - Usa ingredientes corrientes y recetas plausibles.
    - No expliques el proceso.
    - Responde en español.

    Formato obligatorio:
    ## Título de la receta
    **Ingredientes:**
    ...
    **Pasos:**
    ...

    ---
    (separador entre recetas)

    Responde en español.
    No escribas nada fuera de las recetas.

    """
    contador=0
    respuesta=None
    while contador < 5:
        try:
            respuesta = client_gemini.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            break

        except Exception as e:
            contador += 1
            print(f"Intento {contador} falló: {e}")
            await asyncio.sleep(2)

        

    if respuesta is None:
        contador=0
        while contador < 5:
            try:
                respuesta = client_gemini.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )
                break

            except Exception as e:
                contador += 1
                print(f"Intento {contador} falló: {e}")
                await asyncio.sleep(2)


    recetas_separadas = separar_recetas(respuesta.text)
    return {"recetas":recetas_separadas}



