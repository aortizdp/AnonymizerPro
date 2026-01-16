# backend/core/engine.py
import re
import spacy
from .patterns import PATTERNS 

class AnonimitzadorEngine:
    def __init__(self):
        print("--- MOTOR FINAL (ANON + REVERT) ---")
        try:
            self.nlp = spacy.load("es_core_news_lg")
        except:
            self.nlp = spacy.blank("es")

    def processar_text(self, text: str, mapa_global: dict, comptadors: dict):
        # ... (AQUESTA FUNCIÓ ES QUEDA IGUAL QUE ABANS) ...
        # (Copia el codi anterior del processar_text aquí)
        if not isinstance(text, str) or not text.strip():
            return text, mapa_global, comptadors

        canvis = []
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PER" and len(ent.text) > 2:
                if ent.text in mapa_global:
                    token = mapa_global[ent.text]
                else:
                    comptadors["USER"] += 1
                    token = f"%%USER_{comptadors['USER']}%%"
                    mapa_global[ent.text] = token
                canvis.append({'start': ent.start_char, 'end': ent.end_char, 'text': token, 'prio': 1})

        for tipus, regex in PATTERNS.items():
            prioritat = 2 if tipus in ["IBAN", "ID_CARD"] else 3
            for match in re.finditer(regex, text):
                valor_original = match.group()
                start, end = match.start(), match.end()
                if tipus == "ID_CARD" and valor_original.startswith(" "):
                    start += 1
                    valor_original = valor_original.strip()

                if valor_original in mapa_global:
                    token = mapa_global[valor_original]
                else:
                    if tipus not in comptadors:
                        comptadors[tipus] = 0
                    comptadors[tipus] += 1
                    token = f"%%{tipus}_{comptadors[tipus]}%%"
                    mapa_global[valor_original] = token

                canvis.append({'start': start, 'end': end, 'text': token, 'prio': prioritat})

        canvis.sort(key=lambda x: (x['start'], x['prio'], -(x['end']-x['start'])))
        text_list = list(text)
        ultim_index_ocupat = -1
        canvis_valids = []
        for c in canvis:
            if c['start'] >= ultim_index_ocupat:
                canvis_valids.append(c)
                ultim_index_ocupat = c['end']
        canvis_valids.sort(key=lambda x: x['start'], reverse=True)
        for c in canvis_valids:
            text_list[c['start']:c['end']] = list(c['text'])

        return "".join(text_list), mapa_global, comptadors

    # --- NOVA FUNCIÓ PER DESANONIMITZAR ---
    def restaurar_text(self, text: str, diccionari_invers: dict):
        """
        Busca tokens tipus %%USER_1%% i els substitueix pel valor original.
        """
        if not isinstance(text, str):
            return text
            
        # Regex per trobar tokens: %%LLETRES_NUMEROS%%
        tokens_trobats = re.findall(r'%%[A-Z_]+_\d+%%', text)
        
        text_restaurat = text
        for token in tokens_trobats:
            if token in diccionari_invers:
                valor_original = diccionari_invers[token]
                text_restaurat = text_restaurat.replace(token, valor_original)
                
        return text_restaurat
