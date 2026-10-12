import sys
import io
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from backend.allergen_engine import AllergenDetectorEngine
from sample_labels.sample_data import SAMPLE_PRODUCTS

def test_samples():
    print("Running Allergen Detection Tests across multilingual samples...")
    for prod in SAMPLE_PRODUCTS:
        print(f"\n==========================================")
        print(f"Testing Product: {prod['title']}")
        print(f"Language: {prod['primary_language']}")
        
        # Test case 1: User allergic to peanuts
        res_peanut = AllergenDetectorEngine.analyze_label(
            extracted_text=prod["label_text"],
            user_allergens=["peanuts"]
        )
        print(f"Verdict for Peanut-allergic user: {res_peanut['safety_status']} ({res_peanut['verdict_title']})")
        
        # Test case 2: User allergic to gluten
        res_gluten = AllergenDetectorEngine.analyze_label(
            extracted_text=prod["label_text"],
            user_allergens=["gluten"]
        )
        print(f"Verdict for Gluten-allergic user: {res_gluten['safety_status']}")
        
        print(f"Detected INS additives: {[a['name'] for a in res_peanut['additives_profile']]}")
        print(f"NOVA Score: {res_peanut['nova']['score']} ({res_peanut['nova']['title']})")
        print(f"Good effects count: {len(res_peanut['good_effects'])}, Bad effects count: {len(res_peanut['bad_effects'])}")

    print("\nAll engine tests completed successfully!")

if __name__ == "__main__":
    test_samples()
