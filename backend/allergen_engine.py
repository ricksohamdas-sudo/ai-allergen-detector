"""
Biochemical & Food Technology Allergen Detection Engine
Comprehensive knowledge base covering allergens in English, Hindi, and Bengali,
along with biochemical synonyms, cross-contamination detection, and health impact analysis.
"""

import re
from typing import Dict, List, Any, Optional

# Comprehensive Multilingual Allergen Knowledge Base
ALLERGEN_DATABASE: Dict[str, Dict[str, Any]] = {
    "peanuts": {
        "display_name": "Peanuts / Groundnuts",
        "category": "Legumes",
        "bio_protein": "Ara h 1, Ara h 2, Ara h 3, Ara h 6 (2S albumin & cupin superfamily)",
        "anaphylaxis_risk": "VERY HIGH",
        "keywords_en": [
            "peanut", "peanuts", "groundnut", "groundnuts", "monkey nut", "arachis",
            "arachis hypogaea", "arachis oil", "peanut butter", "peanut flour",
            "defatted peanut", "beer nuts"
        ],
        "keywords_hi": [
            "मूंगफली", "मूँगफली", "सींगदाना", "सिंगदाना", "मूंगफली का तेल", "मूंगफली पाउडर"
        ],
        "keywords_bn": [
            "চিনাবাদাম", "চীনা বাদাম", "বাদাম", "চিনাবাদামের তেল", "চীনা বাদামের মাখন"
        ],
        "hidden_derivatives": [
            "hydrolyzed peanut protein", "cold pressed groundnut oil", "mandelonas", "beer nut paste"
        ],
        "clinical_note": "Peanut allergens Ara h 2 and Ara h 6 are highly heat-stable seed storage proteins that resist digestion and commonly trigger severe systemic anaphylaxis."
    },
    "milk": {
        "display_name": "Milk & Dairy (Lactose / Casein / Whey)",
        "category": "Animal Proteins & Disaccharides",
        "bio_protein": "Bos d 4 (α-lactalbumin), Bos d 5 (β-lactoglobulin), Bos d 8 (caseins α/β/κ)",
        "anaphylaxis_risk": "MODERATE TO HIGH",
        "keywords_en": [
            "milk", "dairy", "lactose", "casein", "caseinate", "sodium caseinate",
            "calcium caseinate", "whey", "whey protein", "whey powder", "lactalbumin",
            "lactoglobulin", "butter", "butter oil", "ghee", "cheese", "curd", "yogurt",
            "paneer", "cream", "milk solids", "skimmed milk", "skimmed milk powder",
            "whole milk powder", "condensed milk", "milk fat", "dairy whitener",
            "khoya", "mawa", "buttermilk", "evaporated milk"
        ],
        "keywords_hi": [
            "दूध", "दुग्ध", "पनीर", "घी", "मक्खन", "दही", "मलाई", "खोया", "मावा", "लैक्टोज",
            "व्हे", "केसीन", "मलाई", "छाछ", "दुग्ध ठोस"
        ],
        "keywords_bn": [
            "দুধ", "দুগ্ধ", "ছানা", "পনির", "ঘি", "মাখন", "দই", "মালাই", "খোয়া", "ল্যাকটোজ",
            "হুই প্রোটিন", "কেসিন", "দুধের গুঁড়ো"
        ],
        "hidden_derivatives": [
            "rennet casein", "hydrolyzed whey", "delactosed whey", "galactose", "nougat", "lactylate"
        ],
        "clinical_note": "Distinguishes between IgE-mediated Cow's Milk Protein Allergy (CMPA, reactive to caseins/whey) and non-immune Lactose Intolerance (lactase enzyme insufficiency in small intestine)."
    },
    "gluten": {
        "display_name": "Gluten & Wheat (Celiac / Fructose Malabsorption)",
        "category": "Cereal Prolamins",
        "bio_protein": "Gliadins (α, β, γ, ω) & Glutenins (HMW/LMW) - Wheat; Hordein - Barley; Secalin - Rye",
        "anaphylaxis_risk": "HIGH (Autoimmune Celiac enteropathy & IgE Wheat Anaphylaxis)",
        "keywords_en": [
            "gluten", "wheat", "wheat flour", "refined wheat flour", "maida", "atta",
            "semolina", "suji", "sooji", "rava", "barley", "rye", "malt", "malt extract",
            "spelt", "durum", "triticale", "kamut", "farina", "graham", "seitan",
            "hydrolyzed wheat protein", "wheat germ", "wheat bran", "wheat starch"
        ],
        "keywords_hi": [
            "गेहूं", "मैदा", "सूजी", "आटा", "रवा", "जौ", "माल्ट", "ग्लूटेन", "गेहूं का आटा",
            "परिष्कृत गेहूं का आटा", "सीटन"
        ],
        "keywords_bn": [
            "গম", "ময়দা", "সুজি", "আটা", "বার্লি", "রাই", "মাল্ট", "গ্লুটেন", "গমের আটা",
            "মিহি ময়দা"
        ],
        "hidden_derivatives": [
            "maltodextrin (wheat derived)", "vital wheat gluten", "modified wheat starch", "brewer's yeast"
        ],
        "clinical_note": "Triggers small intestine villous atrophy in Celiac Disease (HLA-DQ2/DQ8 restricted autoimmune response) and exercise-induced anaphylaxis (WDEIA linked to ω5-gliadin)."
    },
    "tree_nuts": {
        "display_name": "Tree Nuts (Cashew, Almond, Pistachio, Walnut)",
        "category": "Botanical Nuts",
        "bio_protein": "Ana o 1-3 (Cashew), Pru du 6 (Almond), Jug r 1-2 (Walnut), Pis v 1-3 (Pistachio)",
        "anaphylaxis_risk": "VERY HIGH",
        "keywords_en": [
            "tree nut", "almond", "cashew", "walnut", "pistachio", "hazelnut", "pecan",
            "macadamia", "brazil nut", "kaju", "badam", "pista", "akhrot", "almond flour",
            "almond milk", "cashew butter", "marzipan", "praline", "gianduja"
        ],
        "keywords_hi": [
            "काजू", "बादाम", "पिस्ता", "अखरोट", "हेज़लनट", "ट्री नट्स", "काजू पेस्ट", "बादाम का दूध"
        ],
        "keywords_bn": [
            "কাজু", "কাজুবাদাম", "কাঠবাদাম", "পেস্তা", "আখরোট", "হেজেলনাট", "বাদাম পেস্ট"
        ],
        "hidden_derivatives": [
            "nut paste", "nut butter", "nut oils (unrefined)", "marzipan", "nougat", "praline"
        ],
        "clinical_note": "Anacardiaceae family (cashew and pistachio) shows very high mutual immunological cross-reactivity. High heat stability across all tree nut storage 2S albumins."
    },
    "soy": {
        "display_name": "Soy & Soya Derivatives",
        "category": "Legumes",
        "bio_protein": "Gly m 5 (β-conglycinin) & Gly m 6 (glycinin - 11S globulin), Gly m 4 (PR-10)",
        "anaphylaxis_risk": "MODERATE",
        "keywords_en": [
            "soy", "soya", "soybean", "edamame", "tofu", "tempeh", "soy lecithin",
            "soya lecithin", "ins 322", "e322", "textured vegetable protein", "tvp",
            "hydrolyzed soy protein", "soy sauce", "tamari", "miso", "soy protein isolate",
            "soy flour", "defatted soy"
        ],
        "keywords_hi": [
            "सोया", "सोयाबीन", "सोया लेसिथिन", "सोया आटा", "सोया सॉस", "टोफू", "सोया प्रोटीन"
        ],
        "keywords_bn": [
            "সোয়া", "সয়াবিন", "সোয়া লেসিথিন", "সোয়া সস", "টোফু", "সোয়াবিন তেল"
        ],
        "hidden_derivatives": [
            "emulsifier (soy lecithin)", "stabilizer ins 322", "vegetable protein (soy)", "kinako"
        ],
        "clinical_note": "Highly refined soybean oil is generally non-allergenic as proteins are removed, but unrefined soy and soy lecithin (INS 322) retain allergen residues."
    },
    "egg": {
        "display_name": "Egg (Albumin / Lysozyme)",
        "category": "Avian Proteins",
        "bio_protein": "Gal d 1 (ovomucoid - heat resistant), Gal d 2 (ovalbumin), Gal d 3 (ovotransferrin), Gal d 4 (lysozyme)",
        "anaphylaxis_risk": "HIGH",
        "keywords_en": [
            "egg", "eggs", "egg white", "egg yolk", "albumin", "ovalbumin", "ovomucoid",
            "ovotransferrin", "lysozyme", "ins 1105", "e1105", "meringue", "mayonnaise",
            "surimi", "globulin", "vitellin", "livetin"
        ],
        "keywords_hi": [
            "अंडा", "अंडे", "अंडे की जर्दी", "अंडे की सफेदी", "एल्बुमिन", "लाइसोजाइम"
        ],
        "keywords_bn": [
            "ডিম", "ডিমের সাদা অংশ", "ডিমের কুসুম", "অ্যালবুমিন", "লাইসোজাইম"
        ],
        "hidden_derivatives": [
            "binder (egg albumin)", "preservative ins 1105", "simplesse", "conalbumin"
        ],
        "clinical_note": "Ovomucoid (Gal d 1) is heavily glycosylated and resistant to heat denaturation and gastric pepsin degradation."
    },
    "mustard": {
        "display_name": "Mustard (Sarson / Rai)",
        "category": "Brassicaceae",
        "bio_protein": "Sin a 1 (Yellow mustard - Sinapis alba), Bra j 1 (Brown/Indian mustard - Brassica juncea)",
        "anaphylaxis_risk": "HIGH (Prevalent in Indian cuisine)",
        "keywords_en": [
            "mustard", "mustard seeds", "mustard oil", "mustard flour", "mustard powder",
            "sinapis", "brassica juncea", "rai", "sarson", "dijon"
        ],
        "keywords_hi": [
            "सरसों", "राई", "सरसों का तेल", "सरसों के दाने", "सरसों पाउडर"
        ],
        "keywords_bn": [
            "সর্ষে", "সরিষা", "সর্ষের তেল", "রাই", "সরিষা বাটা", "সরিষার দানা"
        ],
        "hidden_derivatives": [
            "kachi ghani mustard oil", "mustard paste", "spice blend (contains mustard)"
        ],
        "clinical_note": "2S albumin allergens Sin a 1 and Bra j 1 are major systemic allergens resistant to processing, cooking, and digestive proteolysis."
    },
    "sesame": {
        "display_name": "Sesame (Til / Gingelly)",
        "category": "Pedaliaceae",
        "bio_protein": "Ses i 1 (2S albumin), Ses i 2, Ses i 3 (7S vicilin-like), Ses i 6, Ses i 7 (11S globulins)",
        "anaphylaxis_risk": "VERY HIGH",
        "keywords_en": [
            "sesame", "sesame seeds", "sesame oil", "til", "gingelly", "tahini", "halva",
            "hummus", "sesamum indicum", "benne", "til oil"
        ],
        "keywords_hi": [
            "तिल", "तिल का तेल", "सफेद तिल", "काला तिल", "ताहिनी"
        ],
        "keywords_bn": [
            "তিল", "তিলের তেল", "সাদা তিল", "কালো তিল", "তাহিনি"
        ],
        "hidden_derivatives": [
            "gingelly oil", "til laddu residue", "gomasio", "sesame paste"
        ],
        "clinical_note": "Sesame allergy often manifests with rapid, severe systemic reactions with low eliciting thresholds (< 1 mg protein)."
    },
    "seafood": {
        "display_name": "Fish & Crustaceans (Seafood / Shellfish)",
        "category": "Marine Invertebrates & Teleostei",
        "bio_protein": "Tropomyosin (Pen a 1, Cra c 1 - Crustaceans); Parvalbumin (Gad m 1 - Fish)",
        "anaphylaxis_risk": "VERY HIGH",
        "keywords_en": [
            "fish", "fish oil", "fish gelatin", "shellfish", "prawn", "prawns", "shrimp",
            "crab", "lobster", "crayfish", "clam", "oyster", "mussel", "squid", "calamari",
            "anchovy", "worcestershire", "surimi", "isinglass"
        ],
        "keywords_hi": [
            "मछली", "झींगा", "केकड़ा", "मछली का तेल", "मछली जिलेटिन"
        ],
        "keywords_bn": [
            "মাছ", "চিংড়ি", "গলদা চিংড়ি", "বাগদা চিংড়ি", "কাঁকড়া", "মাছের তেল"
        ],
        "hidden_derivatives": [
            "isinglass (beer fining agent)", "fish sauce", "caesar salad dressing (anchovies)"
        ],
        "clinical_note": "Tropomyosin is a coiled-coil pan-allergen with strong cross-reactivity across shrimp, crabs, lobsters, and dust mites."
    },
    "sulfites": {
        "display_name": "Sulfites & Sulphur Dioxide",
        "category": "Chemical Preservatives",
        "bio_protein": "Non-protein inorganic ion (SO2 / HSO3-); pseudoallergic / neurogenic broncho-constriction",
        "anaphylaxis_risk": "HIGH IN ASTHMATICS",
        "keywords_en": [
            "sulfite", "sulfites", "sulphite", "sulphites", "sulfur dioxide", "sulphur dioxide",
            "sodium metabisulfite", "potassium metabisulfite", "sodium sulfite",
            "ins 220", "ins 221", "ins 222", "ins 223", "ins 224", "ins 226", "ins 227", "ins 228",
            "e220", "e221", "e222", "e223", "e224", "e228"
        ],
        "keywords_hi": [
            "सल्फाइट", "सल्फर डाइऑक्साइड", "सोडियम मेटाबाइसल्फाइट"
        ],
        "keywords_bn": [
            "সালফাইট", "সালফার ডাই অক্সাইড"
        ],
        "hidden_derivatives": [
            "preservative (ins 223)", "bleached starch residue", "dried fruit preservative"
        ],
        "clinical_note": "Inhaled sulfur dioxide gas formed from sulfites triggers parasympathetic reflex bronchospasm in 5-10% of patients with asthma."
    }
}

# Cross-Contamination / Advisory Patterns (strictly for shared equipment / traces)
ADVISORY_PATTERNS = [
    re.compile(r"may\s+contain(?:\s+traces\s+of)?", re.IGNORECASE),
    re.compile(r"manufactured\s+in\s+a\s+facility\s+that\s+also\s+processes", re.IGNORECASE),
    re.compile(r"processed\s+on\s+shared\s+equipment", re.IGNORECASE),
    re.compile(r"made\s+in\s+a\s+factory\s+handling", re.IGNORECASE),
    re.compile(r"packed\s+in\s+the\s+same\s+premises", re.IGNORECASE),
    re.compile(r"traces\s+of", re.IGNORECASE),
    # Hindi advisory patterns
    re.compile(r"अवशेष\s+हो\s+सकते\s+हैं", re.IGNORECASE),
    re.compile(r"उसी\s+संयंत्र\s+में\s+निर्मित", re.IGNORECASE),
    re.compile(r"उसी\s+परिसर\s+में\s+पैक", re.IGNORECASE),
    re.compile(r"संभावित\s+अंश", re.IGNORECASE),
    # Bengali advisory patterns
    re.compile(r"উপস্থিত\s+থাকতে\s+পারে", re.IGNORECASE),
    re.compile(r"একই\s+কারখানায়\s+প্রক্রিয়াজাত", re.IGNORECASE),
    re.compile(r"একই\s+যন্ত্রাংশে\s+উৎপাদিত", re.IGNORECASE),
    re.compile(r"চিহ্ন\s+থাকতে\s+পারে", re.IGNORECASE),
]

# Negation / Allergen-Free Claim Patterns
NEGATION_PATTERNS = [
    re.compile(r"free\s+from", re.IGNORECASE),
    re.compile(r"\-free", re.IGNORECASE),
    re.compile(r"certified\s+gluten\-free", re.IGNORECASE),
    re.compile(r"no\s+added", re.IGNORECASE),
    re.compile(r"does\s+not\s+contain", re.IGNORECASE),
    re.compile(r"zero\s+", re.IGNORECASE),
    re.compile(r"मुक्त", re.IGNORECASE),
]

# Food Additive INS / E-Numbers Biochemical Profiling
FOOD_ADDITIVES_DATABASE: Dict[str, Dict[str, str]] = {
    "102": {
        "name": "Tartrazine (INS 102 / FD&C Yellow 5)",
        "class": "Synthetic Azo Dye (Colorant)",
        "biochemical_effect": "Associated with histamine release, urticaria, and behavioral hyperactivity in sensitive cohorts.",
        "risk_level": "Moderate Risk"
    },
    "110": {
        "name": "Sunset Yellow FCF (INS 110)",
        "class": "Synthetic Azo Dye (Colorant)",
        "biochemical_effect": "Azo linkage can trigger pseudoallergic symptoms, cross-reactivity in aspirin-sensitive individuals.",
        "risk_level": "Moderate Risk"
    },
    "150d": {
        "name": "Caramel Color IV - Ammonia Sulphite Process (INS 150d)",
        "class": "Colorant",
        "biochemical_effect": "Formed at elevated temperatures with ammonia and sulfite compounds; monitored for byproduct 4-Methylimidazole (4-MEI).",
        "risk_level": "Low-Moderate Risk"
    },
    "211": {
        "name": "Sodium Benzoate (INS 211)",
        "class": "Antimicrobial Preservative",
        "biochemical_effect": "Inhibits fungal cell metabolism. When combined with ascorbic acid (Vitamin C) under heat/light, can decarboxylate into trace benzene.",
        "risk_level": "Caution with Vitamin C"
    },
    "220": {
        "name": "Sulphur Dioxide (INS 220)",
        "class": "Antioxidant & Preservative",
        "biochemical_effect": "Allergen warning. Can induce acute severe bronchospasm in asthmatic individuals via cholinergic reflex pathways.",
        "risk_level": "High Allergen Risk"
    },
    "223": {
        "name": "Sodium Metabisulphite (INS 223)",
        "class": "Preservative / Antioxidant / Bleaching agent",
        "biochemical_effect": "Releases sulfur dioxide in aqueous solutions. Potent bronchoconstrictor in sensitive asthmatics.",
        "risk_level": "High Allergen Risk"
    },
    "250": {
        "name": "Sodium Nitrite (INS 250)",
        "class": "Curing Agent / Preservative",
        "biochemical_effect": "Prevents Clostridium botulinum growth; reacts with secondary amines in stomach acid or during high-heat cooking to form carcinogenic nitrosamines.",
        "risk_level": "High Risk on Prolonged High Heat"
    },
    "320": {
        "name": "Butylated Hydroxyanisole / BHA (INS 320)",
        "class": "Synthetic Phenolic Antioxidant",
        "biochemical_effect": "Scavenges lipid peroxyl radicals. Monitored for potential endocrine disruptor mechanisms at elevated cumulative doses.",
        "risk_level": "Moderate Concern"
    },
    "322": {
        "name": "Lecithin (INS 322)",
        "class": "Phospholipid Emulsifier",
        "biochemical_effect": "Phosphatidylcholine surfactant. Allergen alert if derived from unrefined Soy or Egg yolk without proper enzymatic clarification.",
        "risk_level": "Allergen Carrier"
    },
    "471": {
        "name": "Mono- and Diglycerides of Fatty Acids (INS 471)",
        "class": "Emulsifier & Stabilizer",
        "biochemical_effect": "Alters interfacial surface tension in gut. Recent biochemical studies indicate emulsifiers may thin intestinal mucus barrier and alter microbiota.",
        "risk_level": "Moderate Concern (Gut Microbiota)"
    },
    "500": {
        "name": "Sodium Carbonates (INS 500 / Baking Soda)",
        "class": "Acidity Regulator / Leavening Agent",
        "biochemical_effect": "Releases CO2 gas upon thermal decomposition. Generally recognized as safe (GRAS), but contributes to sodium load.",
        "risk_level": "Safe (Contributes to Sodium)"
    },
    "503": {
        "name": "Ammonium Carbonates (INS 503)",
        "class": "Leavening Agent",
        "biochemical_effect": "Thermal dissociation yields ammonia and carbon dioxide. Generally safe in baked goods as ammonia evaporates completely.",
        "risk_level": "Safe"
    },
    "621": {
        "name": "Monosodium Glutamate / MSG (INS 621)",
        "class": "Flavor Enhancer (Umami)",
        "biochemical_effect": "Glutamate salt activating T1R1/T1R3 umami taste receptors. Safe at dietary levels; excessive doses on empty stomach can trigger mild glutamate receptor activation.",
        "risk_level": "Generally Safe (Sensitivity dependent)"
    },
    "951": {
        "name": "Aspartame (INS 951)",
        "class": "Intense Artificial Sweetener",
        "biochemical_effect": "Methyl ester of phenylalanine/aspartic acid dipeptide. Hydrolyzed into phenylalanine (strictly contraindicated in Phenylketonuria / PKU patients).",
        "risk_level": "Contraindicated in PKU"
    },
    "955": {
        "name": "Sucralose (INS 955)",
        "class": "Chlorinated Disaccharide Sweetener",
        "biochemical_effect": "600x sweeter than sucrose, resists enzymatic hydrolysis. May modulate gut microbiome composition and GLP-1 hormone dynamics at high concentrations.",
        "risk_level": "Moderate Concern"
    }
}


class AllergenDetectorEngine:
    """Core analysis engine combining biochemistry rules and multilingual token matching."""

    @staticmethod
    def extract_ins_numbers(text: str) -> List[str]:
        """Detect INS/E-numbers like INS 322, E-211, INS 471(i), etc."""
        matches = re.findall(r"(?:INS|E)[\s\-_]?([0-9]{3,4}[a-z]?(?:\([i-v]+\))?)", text, re.IGNORECASE)
        # Normalize: extract the numeric stem
        stems = set()
        for m in matches:
            num = re.match(r"\d+", m)
            if num:
                stems.add(num.group(0))
        return list(stems)

    @classmethod
    def analyze_label(
        cls,
        extracted_text: str,
        user_allergens: List[str],
        custom_allergen_input: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes biochemical allergen detection and health profiling.
        Returns safety verdict, detected allergen traces, additives profile,
        NOVA level estimate, and biochemical pros/cons.
        """
        text_lower = extracted_text.lower()
        
        # 1. Normalize user allergy list
        active_allergens = set([a.strip().lower() for a in user_allergens if a.strip()])
        if custom_allergen_input:
            custom_splits = [x.strip().lower() for x in re.split(r"[,;]+", custom_allergen_input) if x.strip()]
            active_allergens.update(custom_splits)

        detected_direct_allergens: List[Dict[str, Any]] = []
        detected_advisory_allergens: List[Dict[str, Any]] = []
        all_present_allergens_in_food: List[Dict[str, Any]] = []

        # Check for advisory phrases in label
        has_advisory_context = any(pattern.search(text_lower) for pattern in ADVISORY_PATTERNS)

        # Helper to classify token occurrences across text
        def inspect_token_status(token: str) -> dict:
            tok_pattern = r"\b" + re.escape(token) + r"\b" if token.isascii() else re.escape(token)
            matches = list(re.finditer(tok_pattern, text_lower))
            if not matches:
                matches = list(re.finditer(tok_pattern, extracted_text))
            if not matches:
                return {"found": False, "direct": False, "advisory": False, "negated": False}

            has_direct = False
            has_advisory = False
            all_negated = True

            for m in matches:
                s_idx, e_idx = m.start(), m.end()
                
                # Check line / sentence context for claims
                line_start = text_lower.rfind("\n", 0, s_idx)
                line_start = 0 if line_start == -1 else line_start + 1
                line_end = text_lower.find("\n", e_idx)
                line_end = len(text_lower) if line_end == -1 else line_end
                enclosing_line = text_lower[line_start:line_end]

                # Preceding window up to 140 chars
                w_start = max(0, s_idx - 140)
                w_end = min(len(text_lower), e_idx + 80)
                window = text_lower[w_start:w_end]
                preceding = text_lower[w_start:s_idx]

                # Check prefix negation (e.g. "free from X", "zero X") in preceding text
                preceding_negated = (
                    any(p.search(preceding) for p in NEGATION_PATTERNS) or
                    any(p.search(enclosing_line[:s_idx - line_start]) for p in NEGATION_PATTERNS)
                )

                # Check suffix negation (e.g. "gluten-free", "dairy-free", "ग्लूटेन-मुक्त")
                succeeding = text_lower[e_idx:min(len(text_lower), e_idx + 30)]
                suffix_negated = bool(
                    re.search(r"^[\-\s]?free\b", succeeding, re.IGNORECASE) or
                    re.search(r"^[\-\s]?मुक्त\b", succeeding, re.IGNORECASE) or
                    re.search(r"^[\-\s]?মুক্ত\b", succeeding, re.IGNORECASE)
                )

                is_negated = preceding_negated or suffix_negated

                if is_negated:
                    continue

                all_negated = False
                # Check if inside an advisory clause
                if any(p.search(window) or p.search(enclosing_line) for p in ADVISORY_PATTERNS):
                    has_advisory = True
                else:
                    has_direct = True

            return {
                "found": True,
                "direct": has_direct,
                "advisory": has_advisory,
                "negated": all_negated
            }

        # 2. Iterate through knowledge base allergens
        for key, allergen_data in ALLERGEN_DATABASE.items():
            valid_direct_tokens = []
            valid_advisory_tokens = []

            all_keywords = allergen_data["keywords_en"] + allergen_data["keywords_hi"] + allergen_data["keywords_bn"] + allergen_data["hidden_derivatives"]
            for kw in set(all_keywords):
                status_res = inspect_token_status(kw)
                if status_res["found"] and not status_res["negated"]:
                    if status_res["direct"]:
                        valid_direct_tokens.append(kw)
                    elif status_res["advisory"]:
                        valid_advisory_tokens.append(kw)

            if valid_direct_tokens or valid_advisory_tokens:
                all_tokens = list(set(valid_direct_tokens + valid_advisory_tokens))
                matched_item = {
                    "allergen_key": key,
                    "name": allergen_data["display_name"],
                    "category": allergen_data["category"],
                    "bio_protein": allergen_data["bio_protein"],
                    "matched_tokens": all_tokens,
                    "clinical_note": allergen_data["clinical_note"],
                    "anaphylaxis_risk": allergen_data["anaphylaxis_risk"]
                }
                all_present_allergens_in_food.append(matched_item)

                # Check if this matches user allergy
                user_is_allergic = False
                for ua in active_allergens:
                    if ua in key or key in ua:
                        user_is_allergic = True
                        break
                    all_synonyms = [w.lower() for w in all_keywords]
                    if any(ua in syn or syn in ua for syn in all_synonyms):
                        user_is_allergic = True
                        break

                if user_is_allergic:
                    if valid_direct_tokens:
                        detected_direct_allergens.append(matched_item)
                    elif valid_advisory_tokens:
                        detected_advisory_allergens.append(matched_item)

        # 3. Check for custom allergy strings not in our static database
        for ua in active_allergens:
            # Skip if already in knowledge base
            if any(ua in k or k in ua for k in ALLERGEN_DATABASE.keys()):
                continue
            is_in_db = False
            for db_item in ALLERGEN_DATABASE.values():
                all_syns = [w.lower() for w in db_item["keywords_en"] + db_item["keywords_hi"] + db_item["keywords_bn"]]
                if any(ua in s for s in all_syns):
                    is_in_db = True
                    break
            if is_in_db:
                continue

            if len(ua) > 2:
                custom_status = inspect_token_status(ua)
                if custom_status["found"] and not custom_status["negated"]:
                    custom_match = {
                        "allergen_key": ua,
                        "name": f"Custom Allergen: {ua.capitalize()}",
                        "category": "User-Specified Sensitivity",
                        "bio_protein": "Identified by token match on product label",
                        "matched_tokens": [ua],
                        "clinical_note": "User-defined allergen discovered on ingredient list.",
                        "anaphylaxis_risk": "USER-SPECIFIC"
                    }
                    if custom_status["direct"]:
                        detected_direct_allergens.append(custom_match)
                    elif custom_status["advisory"]:
                        detected_advisory_allergens.append(custom_match)

        # 4. Determine Overall Safety Verdict
        if detected_direct_allergens:
            safety_status = "DANGER"
            verdict_title = "🚨 UNSAFE TO CONSUME - ALLERGEN DETECTED!"
            verdict_color = "red"
            summary_en = f"STOP! This product contains ingredients matching your allergy profile ({', '.join(d['name'] for d in detected_direct_allergens)}). Consuming it poses an immediate risk of an allergic reaction."
            summary_hi = f"सावधान! इस उत्पाद में आपकी एलर्जी से संबंधित घटक मौजूद हैं ({', '.join(d['name'] for d in detected_direct_allergens)})। कृपया इसका सेवन न करें।"
            summary_bn = f"বিপদ! এই খাদ্যটিতে আপনার অ্যালার্জির উপাদান ({', '.join(d['name'] for d in detected_direct_allergens)}) রয়েছে। এটি খাওয়া থেকে বিরত থাকুন।"
        elif detected_advisory_allergens:
            safety_status = "CAUTION"
            verdict_title = "⚠️ CAUTION - CROSS-CONTAMINATION WARNING"
            verdict_color = "orange"
            summary_en = f"CAUTION: May contain trace amounts of ({', '.join(d['name'] for d in detected_advisory_allergens)}) due to shared manufacturing equipment or advisory labeling."
            summary_hi = f"सतर्क रहें! इस उत्पाद में साझा विनिर्माण उपकरण के कारण संभावित अंश हो सकते हैं ({', '.join(d['name'] for d in detected_advisory_allergens)})।"
            summary_bn = f"সতর্কতা! এই খাদ্যটিতে উপাদান উৎপাদনের লাইনে অ্যালার্জেনের উপস্থিতি থাকতে পারে ({', '.join(d['name'] for d in detected_advisory_allergens)})।"
        else:
            safety_status = "SAFE"
            verdict_title = "✅ SAFE TO CONSUME - NO MATCHING ALLERGENS DETECTED"
            verdict_color = "green"
            summary_en = "SAFE: No ingredients or cross-contamination traces matching your specified allergens were detected on this product label."
            summary_hi = "सुरक्षित: इस लेबल पर आपके द्वारा बताई गई किसी भी एलर्जी का कोई घटक नहीं पाया गया।"
            summary_bn = "নিরাপদ: এই পণ্যের লেবেলে আপনার নির্দিষ্ট অ্যালার্জির কোনো উপাদান পাওয়া যায়নি।"

        # 5. Biochemical & Nutritional Profiling (Good & Bad Effects)
        good_effects: List[Dict[str, str]] = []
        bad_effects: List[Dict[str, str]] = []

        # Analyze ingredients for food science biochemical markers
        # Whole grains / dietary fiber
        if any(w in text_lower for w in ["whole wheat", "oats", "bran", "dietary fiber", "millet", "ragi", "bajra", "জোয়ার", "বাজরা", "রাগি"]):
            good_effects.append({
                "factor": "Dietary Fiber & Complex Carbohydrates",
                "biochemical_mechanism": "Provides soluble β-glucan and insoluble cellulose; delays gastric emptying, blunts postprandial glucose spike, and fuels short-chain fatty acid (SCFA: acetate, propionate, butyrate) synthesis by Bifidobacteria."
            })
        
        # High protein / bio-value
        if any(w in text_lower for w in ["protein", "whey isolate", "milk solids", "soya protein", "দুধ", "প্রোটিন", "पनीर"]):
            good_effects.append({
                "factor": "Amino Acid Bioavailability",
                "biochemical_mechanism": "Supplies essential amino acids (Branched-Chain Amino Acids: Leucine, Isoleucine, Valine) supporting mTORC1 activation and myofibrillar protein synthesis."
            })

        # Antioxidants / Natural components
        if any(w in text_lower for w in ["turmeric", "cocoa", "green tea", "tocopherol", "vitamin e", "curcumin", "হলুদ", "हल्दी"]):
            good_effects.append({
                "factor": "Phytochemical & Polyphenolic Activity",
                "biochemical_mechanism": "Scavenges reactive oxygen species (ROS), attenuates lipid peroxidation in cell membranes, and upregulates endogenous Nrf2 antioxidant response elements."
            })

        # Natural fruit / pulp / fermentation
        if any(w in text_lower for w in ["probiotic", "culture", "fermented", "curd", "yogurt", "দই", "दही"]):
            good_effects.append({
                "factor": "Probiotic Fermentation Microecology",
                "biochemical_mechanism": "Introduces viable lactic acid bacteria (Lactobacillus, Streptococcus thermophilus); lowers luminal gut pH, suppressing pathogenic enterobacteria."
            })

        # --- Bad Effects / Biochemical Risks ---
        # High free sugars / Invert syrup / Liquid glucose / HFCS
        if any(w in text_lower for w in ["sugar", "invert syrup", "liquid glucose", "glucose-fructose", "corn syrup", "maltodextrin", "चीनी", "চিনি", "চিনির সিরাপ"]):
            bad_effects.append({
                "factor": "High Glycemic Load & Rapid Fructose Influx",
                "biochemical_mechanism": "Invert sugar and liquid glucose cause rapid pancreatic β-cell insulin spikes. Excess free fructose bypasses phosphofructokinase-1 checkpoint in hepatocytes, stimulating de novo lipogenesis (hepatic steatosis risk)."
            })

        # Hydrogenated vegetable oil / Trans fat / Palm oil
        if any(w in text_lower for w in ["hydrogenated vegetable oil", "vanaspati", "palm oil", "palmolein", "shortening", "वनस्पति", "पाम तेल", "পাম তেল"]):
            bad_effects.append({
                "factor": "Atherogenic Saturated & Trans Fatty Acid Profile",
                "biochemical_mechanism": "High palmitic acid (C16:0) and hydrogenated isomers downregulate LDL receptor transcription, increasing circulating ApoB-containing LDL particles and systemic vascular inflammatory cascades."
            })

        # High sodium / Salt
        if any(w in text_lower for w in ["salt", "sodium", "namak", "नमक", "লবণ", "সোডিয়াম"]):
            bad_effects.append({
                "factor": "Osmotic Hypernatremia & Endothelial Stress",
                "biochemical_mechanism": "Excess dietary sodium shifts fluid homeostasis, enhances renal tubule fluid retention, and transiently impairs endothelial nitric oxide synthase (eNOS) mediated vasodilation."
            })

        # 6. Extract INS Additives & Evaluate
        detected_ins_codes = cls.extract_ins_numbers(extracted_text)
        additives_profile = []
        for code in detected_ins_codes:
            if code in FOOD_ADDITIVES_DATABASE:
                additive_info = FOOD_ADDITIVES_DATABASE[code]
                additives_profile.append(additive_info)
                # Link additive risks to bad effects if notable
                if "Risk" in additive_info["risk_level"] or "Concern" in additive_info["risk_level"]:
                    bad_effects.append({
                        "factor": f"Additive {additive_info['name']}",
                        "biochemical_mechanism": additive_info["biochemical_effect"]
                    })

        # 7. NOVA Ultra-Processed Food (UPF) Classification Estimate
        nova_score = 1
        nova_title = "NOVA Group 1: Unprocessed / Minimally Processed"
        upf_markers = ["maltodextrin", "invert syrup", "ins ", "e322", "hydrogenated", "flavor", "emulsifier", "artificial", "stabilizer"]
        upf_matches = [m for m in upf_markers if m in text_lower]

        if len(upf_matches) >= 3 or detected_ins_codes:
            nova_score = 4
            nova_title = "NOVA Group 4: Ultra-Processed Food (UPF)"
            nova_explanation = "Contains industrial formulations, cosmetic additives, and hydrolyzed substrates not typical of culinary kitchens."
        elif len(upf_matches) >= 1 or any(s in text_lower for s in ["oil", "sugar", "salt"]):
            nova_score = 3
            nova_title = "NOVA Group 3: Processed Food"
            nova_explanation = "Manufactured with culinary additives (sugar, oil, salt) for preservation or texture."
        else:
            nova_explanation = "Whole or naturally preserved foods without industrial cosmetic agents."

        return {
            "safety_status": safety_status,
            "verdict_title": verdict_title,
            "verdict_color": verdict_color,
            "summaries": {
                "en": summary_en,
                "hi": summary_hi,
                "bn": summary_bn
            },
            "detected_direct_allergens": detected_direct_allergens,
            "detected_advisory_allergens": detected_advisory_allergens,
            "all_present_allergens": all_present_allergens_in_food,
            "good_effects": good_effects,
            "bad_effects": bad_effects,
            "additives_profile": additives_profile,
            "nova": {
                "score": nova_score,
                "title": nova_title,
                "explanation": nova_explanation
            }
        }
