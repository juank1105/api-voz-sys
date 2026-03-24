import os
import uuid
import asyncio
import edge_tts
from pydub import AudioSegment
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

class AudioRequest(BaseModel):
    texto: str
    voz: str = "es-CO-SalomeNeural"

@app.post("/generar-audio")
async def generar_audio_api(req: AudioRequest):
    id_audio = str(uuid.uuid4())[:8]
    carpeta_salida = "audios_generados"
    os.makedirs(carpeta_salida, exist_ok=True)
    
    archivo_mp3 = os.path.join(carpeta_salida, f"audio_{id_audio}.mp3")
    archivo_ogg = os.path.join(carpeta_salida, f"audio_{id_audio}.ogg")

    comunicacion = edge_tts.Communicate(req.texto, req.voz)
    await comunicacion.save(archivo_mp3)

    audio = AudioSegment.from_mp3(archivo_mp3)
    audio.export(archivo_ogg, format="ogg", codec="libopus")
    
    if os.path.exists(archivo_mp3):
        os.remove(archivo_mp3)

    return FileResponse(
        path=archivo_ogg, 
        media_type="audio/ogg", 
        filename=f"audio_{id_audio}.ogg"
    )
