import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_drug_info(drug_name: str):
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    prompt = (
        f"ismi detaylı ve karmaşık olan '{drug_name}' ilac ismini ayıklayarak sadece ilacın ismini icerecek sekilde al ve kısa bir prospektüs yaz. "
        "örneğin Parol500g?asdfasfdmasdfkasdmfjasit gibi karmasık bir sey gelebilir. buradan ilac ismi olarak parol olduğunu anlayıp kısa bir açıklama vermelisin. "
        "örnek açıklama şöyle olmalı.Parasetamol içeren ağrı kesici ve ateş düşürücü ilaç. Baş ağrısı, diş ağrısı, kas ağrıları ve ateş için kullanılır. "
        "Günlük maksimum doz 4000mg'dır. bunun gibi kısa ama  bir açıklama ver. maksimum 2 cümle olmalı. "
    )
    response = model.generate_content(prompt)
    return response.text
