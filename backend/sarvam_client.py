"""
Sarvam AI Service Wrapper for AI Allergen Detector
Handles Multilingual Document AI (OCR), LLM Reasoning (Sarvam-105B),
Translation, and Indic Text-to-Speech (Bulbul TTS).
"""

import os
import time
import base64
import requests
from typing import Dict, Any, Optional

try:
    from sarvamai import SarvamAI
    SARVAM_SDK_AVAILABLE = True
except ImportError:
    SARVAM_SDK_AVAILABLE = False


class SarvamService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SARVAM_API_KEY", "")
        self.client = None
        if self.api_key and SARVAM_SDK_AVAILABLE:
            try:
                self.client = SarvamAI(api_subscription_key=self.api_key)
            except Exception as e:
                print(f"Error initializing SarvamAI client: {e}")

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def digitise_document(self, file_bytes: bytes, file_name: str = "label.jpg") -> Dict[str, Any]:
        """
        Digitise label image using Sarvam Document AI API.
        Asynchronously polls for completion and returns extracted text.
        """
        if not self.is_configured():
            return {
                "success": False,
                "error": "Sarvam API Key is not configured. Please enter your key in the sidebar or .env file.",
                "text": ""
            }

        headers = {
            "api-subscription-key": self.api_key
        }

        # Step 1: Submit Digitise job to Sarvam Doc-AI
        url = "https://api.sarvam.ai/doc-ai/v1/job/digitise"
        mime_type = "image/jpeg" if file_name.lower().endswith((".jpg", ".jpeg")) else "image/png"
        files = {
            "file": (file_name, file_bytes, mime_type)
        }
        data = {
            "language": "en-IN"  # Sarvam handles multilingual text automatically
        }

        try:
            response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
            if response.status_code not in (200, 201, 202):
                return {
                    "success": False,
                    "error": f"Sarvam Doc-AI submission failed ({response.status_code}): {response.text}",
                    "text": ""
                }

            job_data = response.json()
            job_id = job_data.get("job_id")
            if not job_id:
                return {
                    "success": False,
                    "error": "Failed to obtain job_id from Sarvam Doc-AI response.",
                    "text": ""
                }

            # Step 2: Poll status
            status_url = f"https://api.sarvam.ai/doc-ai/v1/job/{job_id}/status"
            max_retries = 25
            for _ in range(max_retries):
                time.sleep(2)
                status_resp = requests.get(status_url, headers=headers, timeout=15)
                if status_resp.status_code == 200:
                    status_json = status_resp.json()
                    status = status_json.get("status", "").lower()
                    if status == "completed":
                        # Step 3: Fetch results
                        results_url = f"https://api.sarvam.ai/doc-ai/v1/job/{job_id}/results"
                        res_resp = requests.get(results_url, headers=headers, timeout=15)
                        if res_resp.status_code == 200:
                            res_json = res_resp.json()
                            extracted_text = res_json.get("text", "") or res_json.get("content", "")
                            # If structured pages exist, join them
                            if not extracted_text and "pages" in res_json:
                                extracted_text = "\n".join([p.get("text", "") for p in res_json["pages"]])
                            return {
                                "success": True,
                                "text": extracted_text,
                                "raw_result": res_json
                            }
                    elif status in ("failed", "rejected"):
                        return {
                            "success": False,
                            "error": f"Doc-AI processing failed with status: {status}",
                            "text": ""
                        }
            
            return {
                "success": False,
                "error": "Doc-AI processing timed out while waiting for results.",
                "text": ""
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Network or execution error calling Sarvam Doc-AI: {str(e)}",
                "text": ""
            }

    def chat_analyze_biochemistry(
        self,
        label_text: str,
        user_allergens: list,
        target_lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Uses Sarvam Chat (Sarvam-105B) for deep food science & biochemical reasoning.
        """
        if not self.is_configured():
            return {
                "success": False,
                "response": "API Key not configured. Using rule-based Biochemical Engine."
            }

        lang_instructions = {
            "en": "Respond primarily in clear English.",
            "hi": "Respond in Hindi (हिन्दी) with precise food technology and allergen terminology.",
            "bn": "Respond in Bengali (বাংলা) with precise biochemical and allergen terminology."
        }

        lang_prompt = lang_instructions.get(target_lang, lang_instructions["en"])

        prompt = f"""
You are an expert Food Scientist and Biochemical Engineer specializing in food allergen detection, food labeling laws (FSSAI/FDA/EU), and clinical biochemistry.

Food Product Label Text:
\"\"\"
{label_text}
\"\"\"

Consumer's Known Allergies / Intolerances:
{', '.join(user_allergens)}

Please analyze this food label thoroughly:
1. Allergen Safety Assessment: Is this product SAFE, RISKY (cross-contamination), or DANGEROUS to consume for this individual? Cite the exact ingredients or cross-contamination advisory found on the label.
2. Biochemical Mechanism of the Allergen: Explain which specific protein families or biochemical epitopes (e.g., Ara h storage proteins, Gliadin/Glutenin, Bos d caseins/whey, Gal d ovomucoid) are responsible.
3. Good Effects: Beneficial nutrients (e.g., dietary fiber, whole grains, bioavailable minerals, polyphenols).
4. Bad Effects & Food Additives: Evaluate harmful ingredients like high glycemic sugars (invert syrup, maltodextrin), trans/saturated fats, high sodium, and INS food additives (preservatives, artificial colors, emulsifiers) and their biochemical consequences on human metabolism.
5. Final Clear Directive: A prominent safety advisory for the consumer.

{lang_prompt}
"""
        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sarvam-105b",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an authoritative Biochemical Engineering and Food Science AI assistant for allergen safety."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2
        }

        try:
            resp = requests.post("https://api.sarvam.ai/v1/chat/completions", headers=headers, json=payload, timeout=40)
            if resp.status_code == 200:
                result = resp.json()
                content = result["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "response": content
                }
            else:
                return {
                    "success": False,
                    "response": f"Sarvam Chat API returned error {resp.status_code}: {resp.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error calling Sarvam Chat API: {str(e)}"
            }

    def generate_speech_alert(self, text: str, lang: str = "en") -> Optional[bytes]:
        """
        Synthesize voice alert using Sarvam Bulbul TTS.
        Supports en-IN, hi-IN, bn-IN.
        """
        if not self.is_configured():
            return None

        lang_code_map = {
            "en": "en-IN",
            "hi": "hi-IN",
            "bn": "bn-IN"
        }
        lang_code = lang_code_map.get(lang, "en-IN")

        # Select speaker suited for alerts
        speaker = "shubh" if lang != "bn" else "ananya"

        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }

        # Truncate text to fit within 500 chars for concise spoken warning
        spoken_text = text[:450].strip()

        payload = {
            "text": spoken_text,
            "model": "bulbul:v4-flash",
            "speaker": speaker,
            "language_code": lang_code,
            "pace": 1.05
        }

        try:
            resp = requests.post("https://api.sarvam.ai/text-to-speech", headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                # Sarvam TTS returns either raw audio or JSON with base64 audios
                content_type = resp.headers.get("Content-Type", "")
                if "audio" in content_type:
                    return resp.content
                else:
                    data = resp.json()
                    if "audios" in data and len(data["audios"]) > 0:
                        return base64.b64decode(data["audios"][0])
                    elif "audio" in data:
                        return base64.b64decode(data["audio"])
            return None
        except Exception as e:
            print(f"TTS generation error: {e}")
            return None

    def translate_text(self, text: str, target_lang: str = "hi") -> str:
        """
        Translate text using Sarvam Translation API.
        """
        if not self.is_configured():
            return text

        lang_code_map = {
            "en": "en-IN",
            "hi": "hi-IN",
            "bn": "bn-IN"
        }
        target_code = lang_code_map.get(target_lang, "hi-IN")

        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "input": text[:1000],
            "source_language_code": "en-IN",
            "target_language_code": target_code
        }

        try:
            resp = requests.post("https://api.sarvam.ai/text/translate", headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("translated_text", text)
        except Exception:
            pass
        return text
