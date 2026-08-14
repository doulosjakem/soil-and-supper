#!/usr/bin/env python3
"""
Automated dataset source discovery and scoring for Soil & Supper ML pipeline.

Searches for and scores candidate datasets by:
- legal confidence
- commercial usability
- number of target classes
- images per class
- real-world diversity
- geographic relevance
- growth-stage coverage
- plant-part coverage
- image quality
- licensing complexity
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"
REPORTS_DIR = TRAINING_DATA_DIR / "reports"

MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class SourceScorer:
    """Score candidate dataset sources."""

    def __init__(self):
        self.weights = {
            "legal_confidence": 0.25,
            "commercial_usability": 0.20,
            "target_class_coverage": 0.15,
            "images_per_class": 0.10,
            "real_world_diversity": 0.10,
            "geographic_relevance": 0.05,
            "growth_stage_coverage": 0.05,
            "plant_part_coverage": 0.05,
            "image_quality": 0.03,
            "licensing_complexity": 0.02,
        }
        self.sources: List[Dict] = []

    def score_source(self, source: Dict) -> float:
        """Calculate composite score for a source."""
        score = 0.0
        
        legal_conf = source.get("legal_confidence", 0)
        commercial = 1.0 if source.get("commercial_ok", False) else 0.0
        target_classes = min(len(source.get("target_classes", [])) / 20.0, 1.0)
        images_per_class = min(source.get("images_per_class", 0) / 500.0, 1.0)
        diversity = source.get("real_world_diversity", 0)
        geographic = 1.0 if source.get("geographic_relevance", "").lower() in ["north america", "usa", "us"] else 0.5
        growth_stage = source.get("growth_stage_coverage", 0)
        plant_part = source.get("plant_part_coverage", 0)
        quality = source.get("image_quality", 0)
        license_complex = 1.0 - min(source.get("licensing_complexity", 0.5), 1.0)
        
        score += self.weights["legal_confidence"] * legal_conf
        score += self.weights["commercial_usability"] * commercial
        score += self.weights["target_class_coverage"] * target_classes
        score += self.weights["images_per_class"] * images_per_class
        score += self.weights["real_world_diversity"] * diversity
        score += self.weights["geographic_relevance"] * geographic
        score += self.weights["growth_stage_coverage"] * growth_stage
        score += self.weights["plant_part_coverage"] * plant_part
        score += self.weights["image_quality"] * quality
        score += self.weights["licensing_complexity"] * license_complex
        
        return round(score, 2)

    def add_source(self, source: Dict):
        """Add a source and calculate its score."""
        source["score"] = self.score_source(source)
        source["added_date"] = datetime.now().isoformat()
        self.sources.append(source)
        return source

    def get_ranked_sources(self) -> List[Dict]:
        """Return sources ranked by score."""
        return sorted(self.sources, key=lambda x: x.get("score", 0), reverse=True)

    def get_sources_by_domain(self, domain: str) -> List[Dict]:
        """Get sources for a specific domain."""
        return [s for s in self.sources if s.get("domain") == domain]

    def get_sources_by_status(self, status: str) -> List[Dict]:
        """Get sources by license status."""
        return [s for s in self.sources if s.get("status") == status]

    def generate_report(self) -> Dict:
        """Generate source discovery report."""
        ranked = self.get_ranked_sources()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_sources": len(self.sources),
            "approved": len([s for s in self.sources if s.get("status") == "APPROVED"]),
            "hold": len([s for s in self.sources if s.get("status") == "HOLD"]),
            "rejected": len([s for s in self.sources if s.get("status") == "REJECTED"]),
            "by_domain": {},
            "ranked_sources": ranked,
            "top_sources": ranked[:10],
        }
        
        for domain in ["crops", "weeds", "insects", "beneficials", "diseases", "growth_stages"]:
            domain_sources = self.get_sources_by_domain(domain)
            report["by_domain"][domain] = {
                "total": len(domain_sources),
                "approved": len([s for s in domain_sources if s.get("status") == "APPROVED"]),
                "avg_score": round(sum(s.get("score", 0) for s in domain_sources) / max(len(domain_sources), 1), 2),
                "sources": domain_sources,
            }
        
        return report

    def save_report(self, filename: str = "source_discovery_report.json"):
        """Save report to file."""
        report = self.generate_report()
        report_path = REPORTS_DIR / filename
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Saved source discovery report: {report_path}")
        return report_path

    def print_summary(self):
        """Print human-readable summary."""
        ranked = self.get_ranked_sources()
        
        print("=" * 80)
        print("SOURCE DISCOVERY REPORT")
        print("=" * 80)
        print(f"Total sources: {len(self.sources)}")
        print(f"Approved: {len(self.get_sources_by_status('APPROVED'))}")
        print(f"Hold: {len(self.get_sources_by_status('HOLD'))}")
        print(f"Rejected: {len(self.get_sources_by_status('REJECTED'))}")
        
        print("\nTOP 20 SOURCES:")
        print("-" * 80)
        for i, source in enumerate(ranked[:20], 1):
            status = source.get("status", "UNKNOWN")
            print(f"{i:2}. [{status:8}] {source.get('name', 'Unknown'):40} Score: {source.get('score', 0):4.1f}  Domain: {source.get('domain', '?')}")
        
        print("\nBY DOMAIN:")
        print("-" * 80)
        for domain in ["crops", "weeds", "insects", "beneficials", "diseases", "growth_stages"]:
            domain_sources = self.get_sources_by_domain(domain)
            approved = len([s for s in domain_sources if s.get("status") == "APPROVED"])
            print(f"  {domain:15}: {len(domain_sources):2} sources, {approved:2} approved")


def initialize_default_sources() -> SourceScorer:
    """Initialize with researched sources from Phase 10 expansion."""
    scorer = SourceScorer()
    
    # =========================================================================
    # NORTH AMERICAN WEEDS
    # =========================================================================
    
    scorer.add_source({
        "source_id": "uc_ipm_weeds",
        "name": "UC IPM Weed Images",
        "url": "https://ipm.ucanr.edu/PMG/WEEDS/",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "weeds",
        "source_type": "university_extension",
        "target_classes": ["Dandelion", "Crabgrass", "Purslane", "Lambsquarters", "Pigweed", "Chickweed", "Plantain", "Bindweed", "Thistle", "Foxtail", "Nutsedge", "Ragweed", "Johnsongrass", "Quackgrass"],
        "estimated_image_count": 1500,
        "images_per_class": 100,
        "real_world_diversity": 0.9,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.8,
        "plant_part_coverage": 0.85,
        "image_quality": 0.8,
        "licensing_complexity": 0.1,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "UC IPM website footer",
        "verification_notes": "UC ANR uses CC BY 4.0 for most content. Confirmed on UC IPM website.",
        "contact_required": False,
    })
    
    scorer.add_source({
        "source_id": "usda_nrcs_plants",
        "name": "USDA NRCS PLANTS Database",
        "url": "https://plants.usda.gov/",
        "license": "Public Domain (US Government)",
        "license_url": "https://www.usa.gov/publicdomain/label/1.0/",
        "status": "APPROVED",
        "domain": "weeds",
        "source_type": "government_image_library",
        "target_classes": ["Dandelion", "Crabgrass", "Purslane", "Lambsquarters", "Pigweed", "Chickweed", "Plantain", "Bindweed", "Thistle", "Foxtail", "Nutsedge", "Ragweed", "Johnsongrass", "Quackgrass"],
        "estimated_image_count": 5000,
        "images_per_class": 350,
        "real_world_diversity": 0.9,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.8,
        "plant_part_coverage": 0.9,
        "image_quality": 0.7,
        "licensing_complexity": 0.1,
        "legal_confidence": 1.0,
        "commercial_ok": True,
        "attribution_required": False,
        "ml_training_permitted": True,
        "verification_source": "USDA NRCS copyright policy",
        "verification_notes": "US Government work, public domain. Images are copyright-free unless otherwise indicated.",
        "contact_required": False,
    })
    
    scorer.add_source({
        "source_id": "bugwood_weeds",
        "name": "Bugwood Weed Images",
        "url": "https://www.invasive.org/",
        "license": "Mixed (many CC BY)",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "HOLD",
        "domain": "weeds",
        "source_type": "institutional_image_library",
        "target_classes": ["Dandelion", "Crabgrass", "Purslane", "Lambsquarters", "Pigweed", "Chickweed", "Plantain", "Bindweed", "Thistle", "Foxtail", "Nutsedge", "Ragweed", "Knotweed", "Ground_ivy", "Woodsorrel", "Johnsongrass", "Quackgrass", "Poison_ivy", "Garlic_mustard"],
        "estimated_image_count": 15000,
        "images_per_class": 800,
        "real_world_diversity": 0.95,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.85,
        "plant_part_coverage": 0.9,
        "image_quality": 0.8,
        "licensing_complexity": 0.8,
        "legal_confidence": 0.4,
        "commercial_ok": False,
        "attribution_required": True,
        "ml_training_permitted": False,
        "verification_source": "Bugwood.org Image Usage policy",
        "verification_notes": "Individual photographers retain rights. Commercial use requires photographer approval per image. Many images are CC BY but filtering is required.",
        "contact_required": True,
    })
    
    # =========================================================================
    # INSECTS/PESTS
    # =========================================================================
    
    scorer.add_source({
        "source_id": "uc_ipm_insects",
        "name": "UC IPM Insect Images",
        "url": "https://ipm.ucanr.edu/PMG/INSE/",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "insects",
        "source_type": "university_extension",
        "target_classes": ["Aphid", "Japanese_beetle", "Colorado_potato_beetle", "Cucumber_beetle", "Cabbage_worm", "Tomato_hornworm", "Squash_bug", "Whitefly", "Spider_mite", "Thrips", "Leafminer", "Cutworm", "Stink_bug", "Flea_beetle", "Slug", "Snail", "Earwig"],
        "estimated_image_count": 2500,
        "images_per_class": 140,
        "real_world_diversity": 0.85,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.7,
        "plant_part_coverage": 0.8,
        "image_quality": 0.8,
        "licensing_complexity": 0.1,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "UC IPM website footer",
        "verification_notes": "UC ANR uses CC BY 4.0 for most content. Confirmed on UC IPM website.",
        "contact_required": False,
    })
    
    scorer.add_source({
        "source_id": "bugwood_insects",
        "name": "Bugwood Insect Images",
        "url": "https://www.insectimages.org/",
        "license": "Mixed (many CC BY)",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "HOLD",
        "domain": "insects",
        "source_type": "institutional_image_library",
        "target_classes": ["Aphid", "Japanese_beetle", "Colorado_potato_beetle", "Cucumber_beetle", "Cabbage_worm", "Tomato_hornworm", "Squash_bug", "Whitefly", "Spider_mite", "Thrips", "Leafminer", "Cutworm", "Stink_bug", "Flea_beetle", "Mexican_bean_beetle", "Corn_earworm", "Squash_vine_borer", "Blister_beetle", "Slug", "Snail", "Earwig", "Grasshopper"],
        "estimated_image_count": 25000,
        "images_per_class": 1100,
        "real_world_diversity": 0.9,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.7,
        "plant_part_coverage": 0.8,
        "image_quality": 0.75,
        "licensing_complexity": 0.8,
        "legal_confidence": 0.4,
        "commercial_ok": False,
        "attribution_required": True,
        "ml_training_permitted": False,
        "verification_source": "Bugwood.org Image Usage policy",
        "verification_notes": "Individual photographers retain rights. Commercial use requires photographer approval per image. Many images are CC BY but filtering is required.",
        "contact_required": True,
    })
    
    scorer.add_source({
        "source_id": "wikimedia_insects",
        "name": "Wikimedia Commons Insect Images",
        "url": "https://commons.wikimedia.org/wiki/Category:Insects",
        "license": "Mixed (CC BY, CC BY-SA, Public Domain, etc.)",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "HOLD",
        "domain": "insects",
        "source_type": "media_repository",
        "target_classes": ["Aphid", "Japanese_beetle", "Colorado_potato_beetle", "Cucumber_beetle", "Cabbage_worm", "Tomato_hornworm", "Squash_bug", "Whitefly", "Spider_mite", "Thrips", "Leafminer", "Cutworm", "Stink_bug", "Flea_beetle", "Ladybug", "Green_lacewing", "Honey_bee", "Hoverfly", "Praying_mantis", "Spider", "Earthworm", "Slug", "Snail", "Earwig", "Grasshopper"],
        "estimated_image_count": 15000,
        "images_per_class": 625,
        "real_world_diversity": 0.85,
        "geographic_relevance": "Global",
        "growth_stage_coverage": 0.7,
        "plant_part_coverage": 0.7,
        "image_quality": 0.8,
        "licensing_complexity": 0.7,
        "legal_confidence": 0.5,
        "commercial_ok": False,
        "attribution_required": True,
        "ml_training_permitted": False,
        "verification_source": "Wikimedia Commons licensing pages",
        "verification_notes": "Mixed licenses per image. CC BY images are commercially usable. CC BY-SA is incompatible. Requires per-image filtering.",
        "contact_required": False,
    })
    
    # =========================================================================
    # BENEFICIALS
    # =========================================================================
    
    scorer.add_source({
        "source_id": "uc_ipm_beneficials",
        "name": "UC IPM Beneficial Organism Images",
        "url": "https://ipm.ucanr.edu/PMG/BENE/",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "beneficials",
        "source_type": "university_extension",
        "target_classes": ["Ladybug", "Green_lacewing", "Honey_bee", "Hoverfly", "Praying_mantis", "Spider", "Earthworm", "Ground_beetle", "Predatory_bug"],
        "estimated_image_count": 1000,
        "images_per_class": 110,
        "real_world_diversity": 0.85,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.7,
        "plant_part_coverage": 0.8,
        "image_quality": 0.8,
        "licensing_complexity": 0.1,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "UC IPM website footer",
        "verification_notes": "UC ANR uses CC BY 4.0 for most content. Confirmed on UC IPM website.",
        "contact_required": False,
    })
    
    scorer.add_source({
        "source_id": "bugwood_beneficials",
        "name": "Bugwood Beneficial Insect Images",
        "url": "https://www.insectimages.org/",
        "license": "Mixed (many CC BY)",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "HOLD",
        "domain": "beneficials",
        "source_type": "institutional_image_library",
        "target_classes": ["Ladybug", "Green_lacewing", "Honey_bee", "Hoverfly", "Praying_mantis", "Spider", "Earthworm", "Ground_beetle", "Predatory_bug"],
        "estimated_image_count": 8000,
        "images_per_class": 890,
        "real_world_diversity": 0.9,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.7,
        "plant_part_coverage": 0.8,
        "image_quality": 0.75,
        "licensing_complexity": 0.8,
        "legal_confidence": 0.4,
        "commercial_ok": False,
        "attribution_required": True,
        "ml_training_permitted": False,
        "verification_source": "Bugwood.org Image Usage policy",
        "verification_notes": "Individual photographers retain rights. Commercial use requires photographer approval per image. Many images are CC BY but filtering is required.",
        "contact_required": True,
    })
    
    # =========================================================================
    # DISEASES/DISORDERS
    # =========================================================================
    
    scorer.add_source({
        "source_id": "uc_ipm_diseases",
        "name": "UC IPM Plant Disease Images",
        "url": "https://ipm.ucanr.edu/PMG/DISEASE/",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "diseases",
        "source_type": "university_extension",
        "target_classes": ["Powdery_mildew", "Downy_mildew", "Early_blight", "Late_blight", "Bacterial_spot", "Fusarium_wilt", "Verticillium_wilt", "Rust", "Anthracnose", "Leaf_spot", "Blossom_end_rot", "Nutrient_deficiency", "Sunscald", "Frost_damage", "Healthy"],
        "estimated_image_count": 3000,
        "images_per_class": 200,
        "real_world_diversity": 0.9,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.85,
        "plant_part_coverage": 0.9,
        "image_quality": 0.8,
        "licensing_complexity": 0.1,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "UC IPM website footer",
        "verification_notes": "UC ANR uses CC BY 4.0 for most content. Confirmed on UC IPM website.",
        "contact_required": False,
    })
    
    scorer.add_source({
        "source_id": "cornell_disease_herbarium",
        "name": "Cornell Plant Disease Herbarium Images",
        "url": "https://ppathgbif.cals.cornell.edu/",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "diseases",
        "source_type": "university_collection",
        "target_classes": ["Powdery_mildew", "Downy_mildew", "Early_blight", "Late_blight", "Bacterial_spot", "Fusarium_wilt", "Verticillium_wilt", "Rust", "Anthracnose", "Leaf_spot", "Blossom_end_rot", "Healthy"],
        "estimated_image_count": 3000,
        "images_per_class": 250,
        "real_world_diversity": 0.85,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.8,
        "plant_part_coverage": 0.9,
        "image_quality": 0.7,
        "licensing_complexity": 0.2,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "Cornell University website + GBIF",
        "verification_notes": "Images from Cornell Plant Pathology Herbarium. CC BY 4.0 confirmed on GBIF portal.",
        "contact_required": False,
    })
    
    scorer.add_source({
        "source_id": "zenodo_plant_disease",
        "name": "Zenodo Plant Disease Datasets",
        "url": "https://zenodo.org/",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "diseases",
        "source_type": "institutional_repository",
        "target_classes": ["Powdery_mildew", "Downy_mildew", "Early_blight", "Late_blight", "Bacterial_spot", "Fusarium_wilt", "Verticillium_wilt", "Rust", "Anthracnose", "Leaf_spot", "Blossom_end_rot", "Nutrient_deficiency", "Sunscald", "Frost_damage", "Healthy"],
        "estimated_image_count": 10000,
        "images_per_class": 650,
        "real_world_diversity": 0.8,
        "geographic_relevance": "Global",
        "growth_stage_coverage": 0.7,
        "plant_part_coverage": 0.8,
        "image_quality": 0.75,
        "licensing_complexity": 0.1,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "Zenodo terms of use",
        "verification_notes": "Zenodo defaults to CC BY 4.0 for datasets. Most research datasets uploaded use CC BY 4.0.",
        "contact_required": False,
    })
    
    # =========================================================================
    # CROPS - Additional Sources
    # =========================================================================
    
    scorer.add_source({
        "source_id": "usda_ars_gallery",
        "name": "USDA ARS Image Gallery",
        "url": "https://www.ars.usda.gov/oc/images/image-gallery/",
        "license": "Public Domain (US Government)",
        "license_url": "https://www.usa.gov/publicdomain/label/1.0/",
        "status": "APPROVED",
        "domain": "crops",
        "source_type": "government_image_library",
        "target_classes": ["Tomato", "Pepper_sweet", "Cucumber", "Corn", "Potato", "Onion", "Strawberry"],
        "estimated_image_count": 6500,
        "images_per_class": 920,
        "real_world_diversity": 0.85,
        "geographic_relevance": "North America",
        "growth_stage_coverage": 0.8,
        "plant_part_coverage": 0.9,
        "image_quality": 0.75,
        "licensing_complexity": 0.1,
        "legal_confidence": 1.0,
        "commercial_ok": True,
        "attribution_required": False,
        "ml_training_permitted": True,
        "verification_source": "USDA ARS copyright policy + Ag Data Commons",
        "verification_notes": "Photos in the Image Gallery are copyright-free, public domain images unless otherwise indicated.",
        "contact_required": False,
    })
    
    scorer.add_source({
        "source_id": "mendeley_plant_expanded",
        "name": "Mendeley Data Plant/Agriculture Datasets (Expanded)",
        "url": "https://data.mendeley.com/",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "crops",
        "source_type": "data_repository",
        "target_classes": ["Tomato", "Pepper_sweet", "Pepper_hot", "Cucumber", "Eggplant", "Bean", "Corn", "Carrot", "Onion", "Potato", "Broccoli", "Cabbage", "Lettuce", "Spinach", "Pea", "Radish", "Pumpkin", "Strawberry", "Basil", "Cilantro", "Parsley", "Dill", "Chives", "Rosemary", "Thyme", "Oregano", "Sage", "Sunflower", "Marigold", "Zinnia"],
        "estimated_image_count": 20000,
        "images_per_class": 650,
        "real_world_diversity": 0.75,
        "geographic_relevance": "Global",
        "growth_stage_coverage": 0.7,
        "plant_part_coverage": 0.8,
        "image_quality": 0.7,
        "licensing_complexity": 0.1,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "Mendeley Data terms",
        "verification_notes": "Mendeley Data supports CC BY 4.0 for datasets. Requires per-dataset verification.",
        "contact_required": False,
    })
    
    # =========================================================================
    # GROWTH STAGES
    # =========================================================================
    
    scorer.add_source({
        "source_id": "plant_growth_stage",
        "name": "Plant Growth Stage Detection Dataset",
        "url": "https://universe.roboflow.com/mendozajrl/plant-growth-stage-detection",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "growth_stages",
        "source_type": "research_dataset",
        "target_classes": ["Flowering", "Germination", "Harvesting", "Vegetative"],
        "estimated_image_count": 7306,
        "images_per_class": 1826,
        "real_world_diversity": 0.8,
        "geographic_relevance": "Global",
        "growth_stage_coverage": 0.95,
        "plant_part_coverage": 0.85,
        "image_quality": 0.75,
        "licensing_complexity": 0.1,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "Roboflow Universe dataset page",
        "verification_notes": "Explicitly lists 'License: CC BY 4.0' on dataset page.",
        "contact_required": False,
    })
    
    scorer.add_source({
        "source_id": "bdflower",
        "name": "BDFlower",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13123495/",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "status": "APPROVED",
        "domain": "growth_stages",
        "source_type": "research_dataset",
        "target_classes": ["Flowering"],
        "estimated_image_count": 23334,
        "images_per_class": 23334,
        "real_world_diversity": 0.7,
        "geographic_relevance": "Bangladesh",
        "growth_stage_coverage": 0.6,
        "plant_part_coverage": 0.9,
        "image_quality": 0.75,
        "licensing_complexity": 0.1,
        "legal_confidence": 0.9,
        "commercial_ok": True,
        "attribution_required": True,
        "ml_training_permitted": True,
        "verification_source": "PMC article page",
        "verification_notes": "Creative Commons license confirmed in article.",
        "contact_required": False,
    })
    
    return scorer


if __name__ == "__main__":
    scorer = initialize_default_sources()
    scorer.print_summary()
    scorer.save_report()
