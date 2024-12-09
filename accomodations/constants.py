"""Constants for the accommodations app."""

# Institution choices
INSTITUTIONS = [
    # Public Universities - Traditional
    ("uct", "University of Cape Town"),
    ("wits", "University of the Witwatersrand"),
    ("up", "University of Pretoria"),
    ("su", "Stellenbosch University"),
    ("ukzn", "University of KwaZulu-Natal"),
    ("uj", "University of Johannesburg"),
    ("rhodes", "Rhodes University"),
    ("ufs", "University of the Free State"),
    ("ul", "University of Limpopo"),
    ("nwu", "North-West University"),
    ("univen", "University of Venda"),
    ("wsu", "Walter Sisulu University"),
    ("unisa", "University of South Africa"),
    ("nmu", "Nelson Mandela University"),
    ("unizulu", "University of Zululand"),
    ("ufh", "University of Fort Hare"),
    ("ump", "University of Mpumalanga"),
    ("spu", "Sol Plaatje University"),
    ("tut", "Tshwane University of Technology"),
    ("cput", "Cape Peninsula University of Technology"),
    ("dut", "Durban University of Technology"),
    ("cut", "Central University of Technology"),
    ("vut", "Vaal University of Technology"),
    ("mut", "Mangosuthu University of Technology"),
    ("st_augustine", "St. Augustine College of South Africa"),
    ("milpark", "Milpark Education"),
    ("iie_msa", "IIE Monash South Africa"),
    ("regent", "Regent Business School"),
    ("mancosa", "Management College of Southern Africa"),
    ("afda", "AFDA - The South African School of Motion Picture and Live Performance"),
    ("regenesys", "Regenesys Business School"),
    ("henley", "Henley Business School Africa"),
    ("boston", "Boston City Campus & Business College"),
    ("damelin", "Damelin"),
    ("varsity", "Varsity College"),
    ("rosebank", "Rosebank College"),
    ("imm", "IMM Graduate School of Marketing"),
    ("pearson", "Pearson Institute of Higher Education"),
    ("aaa", "AAA School of Advertising"),
    ("vega", "Vega School"),
    ("daf", "Design Academy of Fashion"),
    ("animation_school", "The Animation School"),
    ("cti", "CTI Education Group"),
    ("belgium_campus", "Belgium Campus ITversity"),
    ("richfield", "Richfield Graduate Institute of Technology"),
    ("healthnicon", "Healthnicon Nursing College"),
    ("life_college", "Life College of Learning"),
    ("netcare", "Netcare Education"),
    ("swgc", "South West Gauteng TVET College"),
    ("ewc", "Ekurhuleni West TVET College"),
    ("false_bay", "False Bay TVET College"),
    ("tnc", "Tshwane North TVET College"),
    ("cjc", "Central Johannesburg TVET College"),
]

# Property type choices
PROPERTY_TYPE_CHOICES = [
    ("residence_hall", "University Residence Hall"),
    ("private_residence", "Private Student Residence"),
    ("shared_apartment", "Shared Apartment"),
    ("studio_apartment", "Studio Apartment"),
    ("flat", "Flat"),
    ("house_share", "House Share"),
    ("host_family", "Host Family"),
    ("commune", "Commune"),
    ("boarding_house", "Boarding House"),
    ("single_room", "Single Room"),
    ("double_room", "Double Room"),
    ("cottage", "Cottage"),
    ("garden_flat", "Garden Flat"),
    ("loft_apartment", "Loft Apartment"),
    ("penthouse", "Penthouse"),
    ("on_campus_residence", "On-Campus Residence"),
    ("off_campus_residence", "Off-Campus Residence"),
    ("student_village", "Student Village"),
    ("guesthouse", "Guesthouse"),
    ("serviced_apartment", "Serviced Apartment"),
]

# Payment method choices
PAYMENT_TYPES = [
    ("bursary", "Bursary"),
    ("nsfas", "NSFAS"),
    ("self_funded", "Self-funded"),
    ("student_loan", "Student Loan"),
]

# Amenity choices
AMENITY_CHOICES = [
    ("wifi", "WiFi Included"),
    ("water_included", "Water Included"),
    ("microwave", "Microwave"),
    ("stove_top", "Stove Top"),
    ("refrigerator", "Refrigerator"),
    ("kettle", "Kettle"),
    ("toaster", "Toaster"),
    ("oven", "Oven"),
    ("washing_machine", "Washing Machine"),
    ("dining_table_chairs", "Dining Table and Chairs"),
    ("couch", "Couch"),
    ("dustbin", "Dustbin"),
    ("washing_line", "Washing Line"),
    ("cutlery", "Cutlery"),
    ("crockery", "Crockery"),
    ("free_laundry", "Free Laundry"),
    ("cleaning_services", "Cleaning Services"),
    ("cctv", "CCTV"),
    ("burglar_bars", "Burglar Bars in Bedrooms"),
    ("electric_fencing", "Electric Fencing"),
    ("on_site_manager", "On-Site Manager"),
    ("security_officer", "Security Officer"),
    ("front_desk", "24h Front Desk"),
    ("wheelchair_access", "Wheelchair Access"),
    ("lift_access", "Lift Access"),
    ("computer_room", "Computer Room"),
    ("gym", "Gym (On Site)"),
    ("garden", "Garden"),
    ("off_street_parking", "Off-Street Parking"),
    ("smart_lock", "Smart Locks"),
    ("study_desk", "Study Desk"),
    ("braai_area", "Braai Area"),
    ("shared_kitchen", "Shared Kitchen"),
    ("kitchenette", "Kitchenette"),
    ("individual_bathrooms", "Private Bathrooms"),
    ("shared_lounge", "Shared Lounge Area"),
    ("bike_rack", "Bike Storage"),
    ("events_space", "Events or Meeting Room"),
    ("study_room", "Study Room"),
    ("library", "Library"),
    ("trash_service", "Trash Collection Service"),
    ("meal_plan", "Meal Plan Available"),
    ("coffee_machine", "Coffee Machine"),
    ("printer_scanner", "Printer - Scanner Available"),
    ("fire_safety", "Fire Alarms - Extinguishers"),
    ("proximity_campus", "Close to Campus"),
    ("proximity_transport", "Close to Public Transport"),
    ("parking", "Parking Spaces"),
    ("air_conditioning", "Air Conditioning"),
    ("heating", "Heating Included"),
    ("pet_friendly", "Pet-Friendly Accommodation"),
]

# Gender choices
GENDER_CHOICES = [
    ("any", "Any Gender"),
    ("female", "Female Only"),
    ("male", "Male Only"),
]
