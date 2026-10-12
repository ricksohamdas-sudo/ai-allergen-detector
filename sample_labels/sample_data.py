"""
Sample Food Product Labels for AI Allergen Detector Demonstration
Contains realistic multilingual (English, Hindi, Bengali) label data and ingredient compositions.
"""

from typing import List, Dict, Any

SAMPLE_PRODUCTS: List[Dict[str, Any]] = [
    {
        "id": "sample_cookie",
        "title": "Nutty Crunch Cookies (English & Hindi)",
        "subtitle": "High-sugar biscuit with hidden peanut & soy allergens",
        "primary_language": "English / Hindi",
        "description": "Popular Indian tea biscuit containing refined flour, trans fats, roasted peanuts, and soy lecithin.",
        "label_text": (
            "INGREDIENTS: Refined Wheat Flour (Maida - 52%), Sugar, Hydrogenated Vegetable Fat "
            "(Vanaspati), Roasted Peanuts (मूंगफली - 14%), Invert Sugar Syrup, Liquid Glucose, "
            "Butter (Milk Fat), Soya Lecithin (INS 322), Leavening Agents [INS 503(ii), INS 500(ii)], "
            "Emulsifier (INS 471), Iodised Salt, Artificial Flavouring Substances (Vanilla, Butter).\n\n"
            "सामग्री: मैदा (52%), चीनी, वनस्पति घी, भुनी हुई मूंगफली (14%), इनवर्ट शुगर सिरप, दूध का मक्खन, "
            "सोया लेसिथिन (INS 322), बेकिंग पाउडर, नमक।\n\n"
            "ALLERGEN ADVICE: Contains Wheat (Gluten), Peanuts (मूंगफली), Milk (दूध), and Soy (सोया). "
            "Manufactured in a facility that also processes Tree Nuts (Cashew, Almond) and Sesame."
        ),
        "typical_allergens": ["peanuts", "gluten", "milk", "soy"],
        "advisory_allergens": ["tree_nuts", "sesame"]
    },
    {
        "id": "sample_chanachur",
        "title": "Royal Bengali Chanachur (বাংলা ও ইংরেজি)",
        "subtitle": "Spicy namkeen snack with Mustard, Peanuts, and Asafoetida (Wheat)",
        "primary_language": "Bengali / English",
        "description": "Authentic Bengali spicy mixture prepared with mustard oil, peanuts, and asafoetida resin.",
        "label_text": (
            "উপাদান (INGREDIENTS): বেসন (Chickpea Flour - 45%), চিনাবাদাম (Peanuts - 18%), খাঁটি সর্ষের তেল "
            "(Mustard Oil - 22%), চিঁড়ে (Flattened Rice), শুকনো লঙ্কা গুঁড়ো, সৈন্ধব লবণ, হলুদ গুঁড়ো, "
            "হিং (Compounded Asafoetida containing Wheat flour / ময়দা), সাইট্রিক অ্যাসিড (INS 330)।\n\n"
            "অ্যালার্জেন সতর্কতা (ALLERGEN ADVICE): এই খাদ্যে চিনাবাদাম (Peanuts), সর্ষে (Mustard) এবং গম/ময়দা (Gluten) "
            "রয়েছে। প্রস্তুতকারক কারখানায় কাজুবাদাম (Cashew) এবং তিল (Sesame) প্রক্রিয়াজাত করা হয় (May contain traces of Cashews and Sesame).\n\n"
            "NET WEIGHT: 200g | FSSAI Lic. No. 12822013000456"
        ),
        "typical_allergens": ["peanuts", "mustard", "gluten"],
        "advisory_allergens": ["tree_nuts", "sesame"]
    },
    {
        "id": "sample_noodles",
        "title": "Masala Instant Noodles (हिन्दी & English)",
        "subtitle": "Ultra-processed wheat noodles with MSG and peanut protein hydrolysate",
        "primary_language": "Hindi / English",
        "description": "Spicy quick noodles with wheat flour, MSG flavor enhancer, and hydrolysed groundnut protein.",
        "label_text": (
            "INGREDIENTS (NOODLES): Refined Wheat Flour (मैदा - 76%), Refined Palm Oil, Iodised Salt, "
            "Wheat Gluten, Mineral (Calcium Carbonate), Thickener (INS 412), Acidity Regulators [INS 501(i), INS 500(i)].\n\n"
            "TASTEMAKER (मसाला मिश्रण): Mixed Spices [Onion powder, Coriander, Turmeric, Cumin, Red Chilli, Black Pepper], "
            "Sugar, Hydrolysed Groundnut Protein (हाइड्रोलाइज्ड मूंगफली प्रोटीन), Flavour Enhancer (INS 621 - MSG), "
            "Soy Sauce Powder (contains Soybeans & Wheat), Palm Oil, Caramel Color (INS 150d), Anticaking Agent (INS 551).\n\n"
            "ALLERGEN WARNING / चेतावनी: Contains Wheat (Gluten), Peanut (मूंगफली), and Soy (सोया)। "
            "May contain traces of Milk solids and Mustard (सरसों)।"
        ),
        "typical_allergens": ["gluten", "peanuts", "soy"],
        "advisory_allergens": ["milk", "mustard"]
    },
    {
        "id": "sample_protein_shake",
        "title": "ProMax Dairy Whey Shake (English & Hindi)",
        "subtitle": "High-protein dairy beverage with Bos d milk proteins and artificial sweeteners",
        "primary_language": "English / Hindi",
        "description": "Fitness beverage rich in whey protein and casein, sweetened with sucralose, strictly contraindicated in CMPA.",
        "label_text": (
            "INGREDIENTS: Water, Skimmed Milk Powder (दुग्ध ठोस - 12%), Whey Protein Concentrate (8%), "
            "Cocoa Powder (Alkalized), Emulsifier [INS 322 (Soy Lecithin)], Stabilizers (INS 407, INS 418), "
            "Acidity Regulators (INS 339), Non-caloric Sweetener [INS 955 - Sucralose], Preservative (INS 202).\n\n"
            "सामग्री: पानी, सप्रेटा दूध पाउडर (12%), व्हे प्रोटीन कॉन्संट्रेट (8%), कोको पाउडर, "
            "सोया लेसिथिन (INS 322), सुक्रालोज (INS 955)।\n\n"
            "ALLERGEN INFORMATION: CONTAINS MILK (DAIRY / LACTOSE / CASEIN) AND SOY. GLUTEN-FREE CERTIFIED. "
            "Not suitable for individuals with Cow's Milk Protein Allergy (CMPA) or Lactose Intolerance."
        ),
        "typical_allergens": ["milk", "soy"],
        "advisory_allergens": []
    },
    {
        "id": "sample_clean_bar",
        "title": "PureHarvest Millet & Seed Energy Bar",
        "subtitle": "Certified allergen-safe, whole-grain, prebiotic superfood bar",
        "primary_language": "English",
        "description": "Clean label snack bar made exclusively from sprouted ragi, dates, and chia seeds in a certified allergen-free facility.",
        "label_text": (
            "INGREDIENTS: Certified Gluten-Free Rolled Oats (38%), Sprouted Finger Millet (Ragi - 22%), "
            "Organic Black Dates Paste (20%), Chia Seeds (8%), Flax Seeds (6%), Sunflower Seed Butter (5%), "
            "Cinnamon Powder, Himalayan Rock Salt, Natural Tocopherols (Vitamin E antioxidant).\n\n"
            "SAFETY COMMITMENT: 100% Free from Peanuts, Tree Nuts, Milk, Dairy, Wheat, Gluten, Soy, Eggs, Fish, "
            "and Sulfites. Manufactured in a dedicated ISO 22000 & HACCP certified Allergen-Free Facility.\n\n"
            "NOVA Group 1 Minimally Processed | High Dietary Fiber (8.4g) | Zero Added Sugar | Zero Preservatives"
        ),
        "typical_allergens": [],
        "advisory_allergens": []
    }
]
