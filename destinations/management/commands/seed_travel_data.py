import sys
from django.core.management.base import BaseCommand
from django.db import transaction
from destinations.models import Destination, Attraction

class Command(BaseCommand):
    help = 'Seeds the database with 25 realistic Indian travel destinations and attractions.'

    def handle(self, *args, **kwargs):
        data = [
            {
                "name": "Agra",
                "description": "Home to the iconic Taj Mahal, Agra is a city rich in Mughal history and architecture.",
                "best_time": "October to March",
                "attractions": [
                    {"name": "Taj Mahal", "category": "Monument", "description": "Iconic ivory-white marble mausoleum on the right bank of the river Yamuna.", "estimated_time": 3.0, "approx_cost": 50, "priority": 5, "latitude": 27.1751, "longitude": 78.0421},
                    {"name": "Agra Fort", "category": "Fort", "description": "Historical fort, residence of the emperors of the Mughal Dynasty.", "estimated_time": 2.5, "approx_cost": 40, "priority": 4, "latitude": 27.1795, "longitude": 78.0211},
                    {"name": "Fatehpur Sikri", "category": "Historical", "description": "A well-preserved red sandstone ghost town.", "estimated_time": 3.0, "approx_cost": 50, "priority": 4, "latitude": 27.0945, "longitude": 77.6679},
                    {"name": "Mehtab Bagh", "category": "Garden", "description": "A charbagh complex offering stunning views of the Taj Mahal at sunset.", "estimated_time": 1.0, "approx_cost": 25, "priority": 3, "latitude": 27.1797, "longitude": 78.0430},
                    {"name": "Akbar's Tomb", "category": "Monument", "description": "The tomb of the Mughal emperor, Akbar.", "estimated_time": 1.5, "approx_cost": 30, "priority": 3, "latitude": 27.2206, "longitude": 77.9505},
                ]
            },
            {
                "name": "Jaipur",
                "description": "The Pink City of India, known for its royal palaces, forts, and vibrant markets.",
                "best_time": "November to February",
                "attractions": [
                    {"name": "Amber Fort", "category": "Fort", "description": "Majestic hilltop fort featuring Hindu style elements.", "estimated_time": 3.0, "approx_cost": 100, "priority": 5, "latitude": 26.9855, "longitude": 75.8513},
                    {"name": "Hawa Mahal", "category": "Palace", "description": "The Palace of Winds, an iconic five-story pink sandstone structure.", "estimated_time": 1.0, "approx_cost": 50, "priority": 5, "latitude": 26.9239, "longitude": 75.8267},
                    {"name": "City Palace", "category": "Palace", "description": "A vast complex of courtyards, gardens, and buildings.", "estimated_time": 2.5, "approx_cost": 150, "priority": 4, "latitude": 26.9255, "longitude": 75.8236},
                    {"name": "Jantar Mantar", "category": "Monument", "description": "An astronomical observation site built in the early 18th century.", "estimated_time": 1.5, "approx_cost": 50, "priority": 3, "latitude": 26.9247, "longitude": 75.8246},
                    {"name": "Nahargarh Fort", "category": "Fort", "description": "Stands on the edge of the Aravalli Hills, overlooking the city.", "estimated_time": 2.0, "approx_cost": 50, "priority": 4, "latitude": 26.9373, "longitude": 75.8155},
                ]
            },
            {
                "name": "Goa",
                "description": "A coastal paradise famous for its sandy beaches, vibrant nightlife, and Portuguese heritage.",
                "best_time": "Mid-November to Mid-February",
                "attractions": [
                    {"name": "Baga Beach", "category": "Beach", "description": "Popular beach known for its water sports and nightlife.", "estimated_time": 4.0, "approx_cost": 500, "priority": 5, "latitude": 15.5553, "longitude": 73.7517},
                    {"name": "Basilica of Bom Jesus", "category": "Church", "description": "UNESCO World Heritage site holding the mortal remains of St. Francis Xavier.", "estimated_time": 1.5, "approx_cost": 0, "priority": 4, "latitude": 15.5009, "longitude": 73.9116},
                    {"name": "Dudhsagar Falls", "category": "Nature", "description": "A four-tiered waterfall located on the Mandovi River.", "estimated_time": 5.0, "approx_cost": 400, "priority": 4, "latitude": 15.3144, "longitude": 74.3143},
                    {"name": "Aguada Fort", "category": "Fort", "description": "A well-preserved seventeenth-century Portuguese fort.", "estimated_time": 2.0, "approx_cost": 0, "priority": 3, "latitude": 15.4925, "longitude": 73.7634},
                    {"name": "Anjuna Beach", "category": "Beach", "description": "Famous for its stunning natural beauty and trance parties.", "estimated_time": 3.0, "approx_cost": 300, "priority": 4, "latitude": 15.5733, "longitude": 73.7408},
                ]
            },
            {
                "name": "Mumbai",
                "description": "India's financial capital, a bustling metropolis that never sleeps.",
                "best_time": "October to February",
                "attractions": [
                    {"name": "Gateway of India", "category": "Monument", "description": "An arch monument built during the 20th century.", "estimated_time": 1.5, "approx_cost": 0, "priority": 5, "latitude": 18.9220, "longitude": 72.8347},
                    {"name": "Marine Drive", "category": "Promenade", "description": "A 3.6-kilometer-long boulevard along the coast.", "estimated_time": 2.0, "approx_cost": 0, "priority": 5, "latitude": 18.9440, "longitude": 72.8227},
                    {"name": "Elephanta Caves", "category": "Caves", "description": "A network of sculpted caves located on Elephanta Island.", "estimated_time": 4.0, "approx_cost": 250, "priority": 4, "latitude": 18.9633, "longitude": 72.9315},
                    {"name": "Chhatrapati Shivaji Terminus", "category": "Monument", "description": "A historic railway station and a UNESCO World Heritage Site.", "estimated_time": 1.0, "approx_cost": 0, "priority": 4, "latitude": 18.9400, "longitude": 72.8347},
                    {"name": "Juhu Beach", "category": "Beach", "description": "One of the most famous and longest beaches in Mumbai.", "estimated_time": 2.5, "approx_cost": 200, "priority": 3, "latitude": 19.0988, "longitude": 72.8267},
                ]
            },
            {
                "name": "Delhi",
                "description": "The capital of India, blending rich history with rapid modernization.",
                "best_time": "October to March",
                "attractions": [
                    {"name": "Red Fort", "category": "Fort", "description": "Historic fort in the city of Delhi that served as the main residence of the Mughal Emperors.", "estimated_time": 2.5, "approx_cost": 35, "priority": 5, "latitude": 28.6562, "longitude": 77.2410},
                    {"name": "Qutub Minar", "category": "Monument", "description": "A UNESCO World Heritage Site and the tallest brick minaret in the world.", "estimated_time": 2.0, "approx_cost": 35, "priority": 5, "latitude": 28.5244, "longitude": 77.1855},
                    {"name": "India Gate", "category": "Monument", "description": "A war memorial located astride the Rajpath.", "estimated_time": 1.0, "approx_cost": 0, "priority": 4, "latitude": 28.6129, "longitude": 77.2295},
                    {"name": "Humayun's Tomb", "category": "Monument", "description": "The tomb of the Mughal Emperor Humayun.", "estimated_time": 2.0, "approx_cost": 35, "priority": 4, "latitude": 28.5933, "longitude": 77.2507},
                    {"name": "Lotus Temple", "category": "Temple", "description": "A Bahá'í House of Worship notable for its flowerlike shape.", "estimated_time": 1.5, "approx_cost": 0, "priority": 3, "latitude": 28.5535, "longitude": 77.2588},
                ]
            },
            {
                "name": "Varanasi",
                "description": "One of the world's oldest continually inhabited cities, the spiritual capital of India.",
                "best_time": "October to March",
                "attractions": [
                    {"name": "Kashi Vishwanath Temple", "category": "Temple", "description": "One of the most famous Hindu temples dedicated to Lord Shiva.", "estimated_time": 2.0, "approx_cost": 0, "priority": 5, "latitude": 25.3109, "longitude": 83.0107},
                    {"name": "Dashashwamedh Ghat", "category": "Ghat", "description": "The main ghat in Varanasi on the Ganga River.", "estimated_time": 2.5, "approx_cost": 0, "priority": 5, "latitude": 25.3068, "longitude": 83.0094},
                    {"name": "Assi Ghat", "category": "Ghat", "description": "The southernmost ghat in Varanasi, popular among tourists.", "estimated_time": 1.5, "approx_cost": 0, "priority": 4, "latitude": 25.2891, "longitude": 83.0055},
                    {"name": "Sarnath", "category": "Historical", "description": "A city located 10 kilometres north-east of Varanasi where Gautama Buddha first taught the Dharma.", "estimated_time": 3.0, "approx_cost": 25, "priority": 4, "latitude": 25.3811, "longitude": 83.0222},
                    {"name": "Ramnagar Fort", "category": "Fort", "description": "A fortification in Ramnagar, Varanasi, built in 1750.", "estimated_time": 2.0, "approx_cost": 50, "priority": 3, "latitude": 25.2699, "longitude": 83.0249},
                ]
            },
            {
                "name": "Udaipur",
                "description": "The City of Lakes, known for its lavish royal residences and artificial lakes.",
                "best_time": "September to March",
                "attractions": [
                    {"name": "City Palace", "category": "Palace", "description": "A palace complex situated in the city of Udaipur.", "estimated_time": 3.0, "approx_cost": 300, "priority": 5, "latitude": 24.5764, "longitude": 73.6835},
                    {"name": "Lake Pichola", "category": "Lake", "description": "An artificial fresh water lake, created in the year 1362 AD.", "estimated_time": 2.0, "approx_cost": 400, "priority": 5, "latitude": 24.5721, "longitude": 73.6788},
                    {"name": "Jag Mandir", "category": "Palace", "description": "A palace built on an island in the Lake Pichola.", "estimated_time": 1.5, "approx_cost": 400, "priority": 4, "latitude": 24.5674, "longitude": 73.6775},
                    {"name": "Fateh Sagar Lake", "category": "Lake", "description": "An artificial lake named after Maharana Fateh Singh.", "estimated_time": 2.0, "approx_cost": 200, "priority": 4, "latitude": 24.6025, "longitude": 73.6750},
                    {"name": "Sajjangarh Monsoon Palace", "category": "Palace", "description": "A hilltop palatial residence overlooking the Fateh Sagar Lake.", "estimated_time": 2.0, "approx_cost": 100, "priority": 3, "latitude": 24.5928, "longitude": 73.6393},
                ]
            },
            {
                "name": "Munnar",
                "description": "A town in the Western Ghats mountain range, surrounded by rolling hills dotted with tea plantations.",
                "best_time": "September to March",
                "attractions": [
                    {"name": "Eravikulam National Park", "category": "Nature", "description": "A national park located along the Western Ghats.", "estimated_time": 4.0, "approx_cost": 120, "priority": 5, "latitude": 10.1667, "longitude": 77.0500},
                    {"name": "Mattupetty Dam", "category": "Dam", "description": "A strong gravity dam which was constructed for power generation and water conservation.", "estimated_time": 2.0, "approx_cost": 50, "priority": 4, "latitude": 10.1064, "longitude": 77.1234},
                    {"name": "Tea Museum", "category": "Museum", "description": "A museum highlighting the history of tea plantations in Munnar.", "estimated_time": 1.5, "approx_cost": 75, "priority": 4, "latitude": 10.0933, "longitude": 77.0538},
                    {"name": "Echo Point", "category": "Nature", "description": "A scenic spot known for its natural echo phenomenon.", "estimated_time": 1.0, "approx_cost": 0, "priority": 3, "latitude": 10.1333, "longitude": 77.1667},
                    {"name": "Pothamedu View Point", "category": "Viewpoint", "description": "Offers panoramic views of the tea, coffee and cardamom plantations.", "estimated_time": 1.0, "approx_cost": 0, "priority": 3, "latitude": 10.0638, "longitude": 77.0427},
                ]
            },
            {
                "name": "Leh",
                "description": "A high-desert city in the Himalayas, known for its Buddhist sites and trekking areas.",
                "best_time": "April to July",
                "attractions": [
                    {"name": "Pangong Lake", "category": "Lake", "description": "An endorheic lake in the Himalayas situated at a height of about 4,350 m.", "estimated_time": 8.0, "approx_cost": 500, "priority": 5, "latitude": 33.7431, "longitude": 78.7303},
                    {"name": "Nubra Valley", "category": "Nature", "description": "A tri-armed valley located to the north east of Ladakh valley.", "estimated_time": 8.0, "approx_cost": 500, "priority": 5, "latitude": 34.6853, "longitude": 77.5542},
                    {"name": "Magnetic Hill", "category": "Nature", "description": "A gravity hill located near Leh in Ladakh.", "estimated_time": 1.0, "approx_cost": 0, "priority": 4, "latitude": 34.1725, "longitude": 77.3517},
                    {"name": "Shanti Stupa", "category": "Monument", "description": "A Buddhist white-domed stupa on a hilltop in Chanspa.", "estimated_time": 1.5, "approx_cost": 0, "priority": 4, "latitude": 34.1755, "longitude": 77.5752},
                    {"name": "Thiksey Monastery", "category": "Monastery", "description": "A gompa affiliated with the Gelug sect of Tibetan Buddhism.", "estimated_time": 2.0, "approx_cost": 30, "priority": 3, "latitude": 34.0560, "longitude": 77.6678},
                ]
            },
            {
                "name": "Darjeeling",
                "description": "A town in India's West Bengal state, in the Himalayan foothills, famous for its black tea.",
                "best_time": "April to June",
                "attractions": [
                    {"name": "Tiger Hill", "category": "Viewpoint", "description": "Famous for its panoramic views of Mount Everest and Mount Kanchenjunga.", "estimated_time": 3.0, "approx_cost": 50, "priority": 5, "latitude": 26.9946, "longitude": 88.2619},
                    {"name": "Batasia Loop", "category": "Monument", "description": "A spiral railway created to lower the gradient of ascent of the Darjeeling Himalayan Railway.", "estimated_time": 1.0, "approx_cost": 20, "priority": 4, "latitude": 27.0142, "longitude": 88.2472},
                    {"name": "Darjeeling Himalayan Railway", "category": "Transport", "description": "A 2 ft gauge railway that runs between New Jalpaiguri and Darjeeling.", "estimated_time": 4.0, "approx_cost": 1500, "priority": 5, "latitude": 27.0427, "longitude": 88.2657},
                    {"name": "Peace Pagoda", "category": "Monument", "description": "A Buddhist stupa designed to provide a focus for people of all races and creeds.", "estimated_time": 1.0, "approx_cost": 0, "priority": 3, "latitude": 27.0345, "longitude": 88.2573},
                    {"name": "Padmaja Naidu Himalayan Zoological Park", "category": "Zoo", "description": "A 67.56-acre zoo in the town of Darjeeling.", "estimated_time": 2.5, "approx_cost": 60, "priority": 4, "latitude": 27.0583, "longitude": 88.2530},
                ]
            },
            {
                "name": "Port Blair",
                "description": "The capital city of the Andaman and Nicobar Islands, an Indian territory in the Bay of Bengal.",
                "best_time": "October to May",
                "attractions": [
                    {"name": "Cellular Jail", "category": "Monument", "description": "A colonial prison used by the British to exile political prisoners.", "estimated_time": 3.0, "approx_cost": 30, "priority": 5, "latitude": 11.6738, "longitude": 92.7480},
                    {"name": "Radhanagar Beach", "category": "Beach", "description": "Known as one of the best beaches in Asia, located on Havelock Island.", "estimated_time": 5.0, "approx_cost": 500, "priority": 5, "latitude": 11.9833, "longitude": 92.9500},
                    {"name": "Ross Island", "category": "Historical", "description": "An island which was the administrative headquarters of the British.", "estimated_time": 3.0, "approx_cost": 300, "priority": 4, "latitude": 11.6750, "longitude": 92.7630},
                    {"name": "Havelock Island", "category": "Island", "description": "Part of Ritchie's Archipelago, known for its dive sites and beaches.", "estimated_time": 8.0, "approx_cost": 1500, "priority": 4, "latitude": 11.9761, "longitude": 92.9876},
                    {"name": "Baratang Island", "category": "Island", "description": "Known for its mangrove creeks, mud volcanoes and limestone caves.", "estimated_time": 6.0, "approx_cost": 1000, "priority": 3, "latitude": 12.1667, "longitude": 92.7500},
                ]
            },
            {
                "name": "Shimla",
                "description": "The capital of the northern Indian state of Himachal Pradesh, in the Himalayan foothills.",
                "best_time": "March to June",
                "attractions": [
                    {"name": "The Ridge", "category": "Promenade", "description": "A large open space, located in the center of Shimla.", "estimated_time": 2.0, "approx_cost": 0, "priority": 5, "latitude": 31.1048, "longitude": 77.1744},
                    {"name": "Mall Road", "category": "Market", "description": "The main street in Shimla, constructed during British colonial rule.", "estimated_time": 3.0, "approx_cost": 500, "priority": 5, "latitude": 31.1042, "longitude": 77.1714},
                    {"name": "Jakhu Temple", "category": "Temple", "description": "An ancient temple dedicated to Hindu deity, Hanuman.", "estimated_time": 2.0, "approx_cost": 0, "priority": 4, "latitude": 31.1011, "longitude": 77.1824},
                    {"name": "Christ Church", "category": "Church", "description": "The second oldest church in North India.", "estimated_time": 1.0, "approx_cost": 0, "priority": 4, "latitude": 31.1045, "longitude": 77.1755},
                    {"name": "Kufri", "category": "Nature", "description": "A small hill station in Shimla district, known for its ski slopes.", "estimated_time": 4.0, "approx_cost": 500, "priority": 3, "latitude": 31.0967, "longitude": 77.2667},
                ]
            },
            {
                "name": "Manali",
                "description": "A high-altitude Himalayan resort town in India's northern Himachal Pradesh state.",
                "best_time": "October to June",
                "attractions": [
                    {"name": "Rohtang Pass", "category": "Nature", "description": "A high mountain pass on the eastern Pir Panjal Range.", "estimated_time": 6.0, "approx_cost": 1000, "priority": 5, "latitude": 32.3716, "longitude": 77.2466},
                    {"name": "Solang Valley", "category": "Nature", "description": "A side valley at the top of the Kullu Valley, known for summer and winter sports.", "estimated_time": 4.0, "approx_cost": 500, "priority": 5, "latitude": 32.3167, "longitude": 77.1500},
                    {"name": "Hidimba Devi Temple", "category": "Temple", "description": "Locally known as Dhungari Temple, dedicated to Hidimbi Devi.", "estimated_time": 1.5, "approx_cost": 0, "priority": 4, "latitude": 32.2474, "longitude": 77.1818},
                    {"name": "Manu Temple", "category": "Temple", "description": "A temple dedicated to the sage Manu, located in Old Manali.", "estimated_time": 1.0, "approx_cost": 0, "priority": 3, "latitude": 32.2536, "longitude": 77.1770},
                    {"name": "Beas River", "category": "Nature", "description": "A river in north India that offers white water rafting.", "estimated_time": 2.0, "approx_cost": 1000, "priority": 4, "latitude": 32.2400, "longitude": 77.1900},
                ]
            },
            {
                "name": "Ooty",
                "description": "A resort town in the Western Ghats mountains, in southern India's Tamil Nadu state.",
                "best_time": "October to June",
                "attractions": [
                    {"name": "Ooty Botanical Gardens", "category": "Garden", "description": "A 55-hectare botanical garden located on the slopes of the Doddabetta peak.", "estimated_time": 2.5, "approx_cost": 30, "priority": 5, "latitude": 11.4186, "longitude": 76.7111},
                    {"name": "Ooty Lake", "category": "Lake", "description": "An artificial lake constructed by John Sullivan, in 1824.", "estimated_time": 2.0, "approx_cost": 150, "priority": 5, "latitude": 11.4024, "longitude": 76.6908},
                    {"name": "Nilgiri Mountain Railway", "category": "Transport", "description": "A 1,000 mm metre gauge railway in Tamil Nadu built by the British.", "estimated_time": 4.0, "approx_cost": 300, "priority": 4, "latitude": 11.4116, "longitude": 76.7022},
                    {"name": "Doddabetta Peak", "category": "Viewpoint", "description": "The highest mountain in the Nilgiri Mountains.", "estimated_time": 2.0, "approx_cost": 10, "priority": 4, "latitude": 11.4011, "longitude": 76.7356},
                    {"name": "Rose Garden", "category": "Garden", "description": "The largest rose garden in India.", "estimated_time": 1.5, "approx_cost": 30, "priority": 3, "latitude": 11.4061, "longitude": 76.7122},
                ]
            },
            {
                "name": "Jaisalmer",
                "description": "A former medieval trading center and a princely state in the western Indian state of Rajasthan.",
                "best_time": "October to March",
                "attractions": [
                    {"name": "Jaisalmer Fort", "category": "Fort", "description": "Situated in the city of Jaisalmer, it is one of the very few 'living forts' in the world.", "estimated_time": 3.0, "approx_cost": 50, "priority": 5, "latitude": 26.9128, "longitude": 70.9133},
                    {"name": "Sam Sand Dunes", "category": "Nature", "description": "The most authentic desert dune site in whole India.", "estimated_time": 4.0, "approx_cost": 500, "priority": 5, "latitude": 26.8333, "longitude": 70.5333},
                    {"name": "Patwon Ki Haveli", "category": "Historical", "description": "A cluster of five large havelis in Jaisalmer.", "estimated_time": 1.5, "approx_cost": 100, "priority": 4, "latitude": 26.9150, "longitude": 70.9161},
                    {"name": "Gadisar Lake", "category": "Lake", "description": "An artificial lake built in the 14th century.", "estimated_time": 1.5, "approx_cost": 50, "priority": 4, "latitude": 26.9081, "longitude": 70.9250},
                    {"name": "Kuldhara Village", "category": "Historical", "description": "An abandoned village in the Jaisalmer district.", "estimated_time": 2.0, "approx_cost": 50, "priority": 3, "latitude": 26.8667, "longitude": 70.7833},
                ]
            },
            {
                "name": "Rishikesh",
                "description": "A city in India's northern state of Uttarakhand, in the Himalayan foothills beside the Ganges River.",
                "best_time": "September to November, February to March",
                "attractions": [
                    {"name": "Triveni Ghat", "category": "Ghat", "description": "A sacred ghat in Rishikesh famous for the Ganga Aarti.", "estimated_time": 2.0, "approx_cost": 0, "priority": 5, "latitude": 30.1030, "longitude": 78.2936},
                    {"name": "Lakshman Jhula", "category": "Monument", "description": "An iron suspension bridge across the river Ganges.", "estimated_time": 1.5, "approx_cost": 0, "priority": 5, "latitude": 30.1228, "longitude": 78.3244},
                    {"name": "Parmarth Niketan", "category": "Ashram", "description": "An ashram situated on the banks of the Ganges.", "estimated_time": 2.0, "approx_cost": 0, "priority": 4, "latitude": 30.1172, "longitude": 78.3142},
                    {"name": "Neelkanth Mahadev Temple", "category": "Temple", "description": "A Hindu temple dedicated to Nilkanth, an aspect of Shiva.", "estimated_time": 3.0, "approx_cost": 0, "priority": 4, "latitude": 30.0768, "longitude": 78.3429},
                    {"name": "Beatles Ashram", "category": "Ashram", "description": "The ashram where the Beatles stayed in 1968.", "estimated_time": 2.0, "approx_cost": 150, "priority": 3, "latitude": 30.1147, "longitude": 78.3156},
                ]
            },
            {
                "name": "Hampi",
                "description": "An ancient village in the south Indian state of Karnataka, dotted with numerous ruined temple complexes from the Vijayanagara Empire.",
                "best_time": "October to February",
                "attractions": [
                    {"name": "Virupaksha Temple", "category": "Temple", "description": "A temple dedicated to Lord Virupaksha, a form of Shiva.", "estimated_time": 2.0, "approx_cost": 50, "priority": 5, "latitude": 15.3350, "longitude": 76.4600},
                    {"name": "Vijaya Vittala Temple", "category": "Temple", "description": "An ancient temple famous for its musical pillars and stone chariot.", "estimated_time": 3.0, "approx_cost": 40, "priority": 5, "latitude": 15.3385, "longitude": 76.4735},
                    {"name": "Matanga Hill", "category": "Viewpoint", "description": "The highest point in Hampi, offering panoramic views of the ruins.", "estimated_time": 2.0, "approx_cost": 0, "priority": 4, "latitude": 15.3331, "longitude": 76.4667},
                    {"name": "Lotus Mahal", "category": "Monument", "description": "A distinctively shaped pavilion within the Zenana Enclosure.", "estimated_time": 1.0, "approx_cost": 40, "priority": 4, "latitude": 15.3204, "longitude": 76.4633},
                    {"name": "Elephant Stables", "category": "Monument", "description": "A large dome-shaped building used to house royal elephants.", "estimated_time": 1.5, "approx_cost": 40, "priority": 3, "latitude": 15.3214, "longitude": 76.4650},
                ]
            },
            {
                "name": "Mysore",
                "description": "A city in India's southwestern Karnataka state, known for its royal heritage and magnificent buildings.",
                "best_time": "October to February",
                "attractions": [
                    {"name": "Mysore Palace", "category": "Palace", "description": "A historical palace and a royal residence.", "estimated_time": 3.0, "approx_cost": 100, "priority": 5, "latitude": 12.3051, "longitude": 76.6551},
                    {"name": "Chamundi Hill", "category": "Temple", "description": "A hill featuring the Chamundeshwari Temple at its summit.", "estimated_time": 2.5, "approx_cost": 0, "priority": 4, "latitude": 12.2740, "longitude": 76.6710},
                    {"name": "Brindavan Gardens", "category": "Garden", "description": "A garden adjoining the Krishnarajasagara Dam.", "estimated_time": 2.0, "approx_cost": 50, "priority": 4, "latitude": 12.4261, "longitude": 76.5736},
                    {"name": "Mysore Zoo", "category": "Zoo", "description": "A 157-acre zoo located near the palace.", "estimated_time": 3.0, "approx_cost": 100, "priority": 3, "latitude": 12.3025, "longitude": 76.6639},
                    {"name": "Jaganmohan Palace", "category": "Palace", "description": "A palace that now serves as an art gallery.", "estimated_time": 1.5, "approx_cost": 40, "priority": 3, "latitude": 12.3061, "longitude": 76.6508},
                ]
            },
            {
                "name": "Kolkata",
                "description": "The capital of India's West Bengal state, known for its grand colonial architecture and art galleries.",
                "best_time": "October to March",
                "attractions": [
                    {"name": "Victoria Memorial", "category": "Monument", "description": "A large marble building dedicated to the memory of Queen Victoria.", "estimated_time": 2.5, "approx_cost": 30, "priority": 5, "latitude": 22.5448, "longitude": 88.3426},
                    {"name": "Howrah Bridge", "category": "Monument", "description": "A balanced cantilever bridge over the Hooghly River.", "estimated_time": 1.0, "approx_cost": 0, "priority": 5, "latitude": 22.5851, "longitude": 88.3468},
                    {"name": "Dakshineswar Kali Temple", "category": "Temple", "description": "A Hindu navaratna temple situated on the eastern bank of the Hooghly River.", "estimated_time": 2.0, "approx_cost": 0, "priority": 4, "latitude": 22.6543, "longitude": 88.3575},
                    {"name": "Indian Museum", "category": "Museum", "description": "The largest and oldest museum in India.", "estimated_time": 3.0, "approx_cost": 50, "priority": 4, "latitude": 22.5579, "longitude": 88.3511},
                    {"name": "Eden Gardens", "category": "Stadium", "description": "A historic cricket ground.", "estimated_time": 1.5, "approx_cost": 0, "priority": 3, "latitude": 22.5646, "longitude": 88.3433},
                ]
            },
            {
                "name": "Hyderabad",
                "description": "The capital of southern India's Telangana state, known as the City of Pearls.",
                "best_time": "October to March",
                "attractions": [
                    {"name": "Charminar", "category": "Monument", "description": "A monument and mosque constructed in 1591.", "estimated_time": 1.5, "approx_cost": 25, "priority": 5, "latitude": 17.3616, "longitude": 78.4747},
                    {"name": "Golconda Fort", "category": "Fort", "description": "A fortified citadel and an early capital city of the Qutb Shahi dynasty.", "estimated_time": 3.0, "approx_cost": 25, "priority": 5, "latitude": 17.3833, "longitude": 78.4011},
                    {"name": "Ramoji Film City", "category": "Theme Park", "description": "An integrated film studio complex and theme park.", "estimated_time": 6.0, "approx_cost": 1500, "priority": 4, "latitude": 17.2543, "longitude": 78.6808},
                    {"name": "Salar Jung Museum", "category": "Museum", "description": "An art museum situated on the southern bank of the Musi River.", "estimated_time": 3.0, "approx_cost": 50, "priority": 4, "latitude": 17.3714, "longitude": 78.4804},
                    {"name": "Hussain Sagar", "category": "Lake", "description": "A heart-shaped lake built by Ibrahim Quli Qutb Shah.", "estimated_time": 2.0, "approx_cost": 0, "priority": 3, "latitude": 17.4239, "longitude": 78.4738},
                ]
            },
            {
                "name": "Chennai",
                "description": "On the Bay of Bengal in eastern India, the capital of the state of Tamil Nadu.",
                "best_time": "November to February",
                "attractions": [
                    {"name": "Marina Beach", "category": "Beach", "description": "A natural urban beach along the Bay of Bengal.", "estimated_time": 2.5, "approx_cost": 0, "priority": 5, "latitude": 13.0475, "longitude": 80.2824},
                    {"name": "Kapaleeshwarar Temple", "category": "Temple", "description": "A Hindu temple dedicated to lord Shiva located in Mylapore.", "estimated_time": 1.5, "approx_cost": 0, "priority": 4, "latitude": 13.0335, "longitude": 80.2701},
                    {"name": "Fort St. George", "category": "Fort", "description": "The first English fortress in India, founded in 1644.", "estimated_time": 2.0, "approx_cost": 15, "priority": 4, "latitude": 13.0805, "longitude": 80.2826},
                    {"name": "Government Museum", "category": "Museum", "description": "A museum of human history and culture.", "estimated_time": 2.5, "approx_cost": 50, "priority": 3, "latitude": 13.0722, "longitude": 80.2570},
                    {"name": "Santhome Cathedral", "category": "Church", "description": "A Catholic minor basilica built over the tomb of Thomas the Apostle.", "estimated_time": 1.0, "approx_cost": 0, "priority": 3, "latitude": 13.0333, "longitude": 80.2778},
                ]
            },
            {
                "name": "Bangalore",
                "description": "The capital of India's southern Karnataka state, known as the Silicon Valley of India.",
                "best_time": "October to February",
                "attractions": [
                    {"name": "Lalbagh Botanical Garden", "category": "Garden", "description": "An old botanical garden, featuring a famous glass house.", "estimated_time": 2.5, "approx_cost": 25, "priority": 5, "latitude": 12.9507, "longitude": 77.5848},
                    {"name": "Bangalore Palace", "category": "Palace", "description": "A royal palace inspired by England's Windsor Castle.", "estimated_time": 2.0, "approx_cost": 250, "priority": 4, "latitude": 12.9988, "longitude": 77.5921},
                    {"name": "Cubbon Park", "category": "Park", "description": "A major sightseeing attraction rich in flora and fauna.", "estimated_time": 2.0, "approx_cost": 0, "priority": 4, "latitude": 12.9779, "longitude": 77.5952},
                    {"name": "Vidhana Soudha", "category": "Monument", "description": "The seat of the state legislature of Karnataka.", "estimated_time": 1.0, "approx_cost": 0, "priority": 3, "latitude": 12.9796, "longitude": 77.5906},
                    {"name": "ISKCON Temple", "category": "Temple", "description": "A large ISKCON temple complex in Rajajinagar.", "estimated_time": 1.5, "approx_cost": 0, "priority": 3, "latitude": 13.0098, "longitude": 77.5511},
                ]
            },
            {
                "name": "Pune",
                "description": "A sprawling city in the western Indian state of Maharashtra, known as the Oxford of the East.",
                "best_time": "October to February",
                "attractions": [
                    {"name": "Aga Khan Palace", "category": "Historical", "description": "A majestic palace which served as a prison for Mahatma Gandhi.", "estimated_time": 2.0, "approx_cost": 25, "priority": 5, "latitude": 18.5524, "longitude": 73.9015},
                    {"name": "Shaniwar Wada", "category": "Fort", "description": "A historical fortification built in 1732.", "estimated_time": 1.5, "approx_cost": 25, "priority": 4, "latitude": 18.5195, "longitude": 73.8553},
                    {"name": "Sinhagad Fort", "category": "Fort", "description": "An ancient hill fortress located around 30 km southwest of the city.", "estimated_time": 3.0, "approx_cost": 50, "priority": 4, "latitude": 18.3663, "longitude": 73.7559},
                    {"name": "Dagdusheth Halwai Ganpati Temple", "category": "Temple", "description": "A popular Hindu temple dedicated to the God Ganesha.", "estimated_time": 1.0, "approx_cost": 0, "priority": 5, "latitude": 18.5164, "longitude": 73.8560},
                    {"name": "Pataleshwar Cave Temple", "category": "Temple", "description": "An 8th century rock-cut cave temple.", "estimated_time": 1.0, "approx_cost": 0, "priority": 3, "latitude": 18.5284, "longitude": 73.8471},
                ]
            },
            {
                "name": "Amritsar",
                "description": "A city in the northwestern Indian state of Punjab, home to the spectacular Golden Temple.",
                "best_time": "November to March",
                "attractions": [
                    {"name": "Golden Temple", "category": "Temple", "description": "The holiest Gurdwara and the most important pilgrimage site of Sikhism.", "estimated_time": 3.0, "approx_cost": 0, "priority": 5, "latitude": 31.6200, "longitude": 74.8765},
                    {"name": "Jallianwala Bagh", "category": "Historical", "description": "A historic garden and memorial of national importance.", "estimated_time": 1.5, "approx_cost": 0, "priority": 5, "latitude": 31.6205, "longitude": 74.8800},
                    {"name": "Wagah Border", "category": "Monument", "description": "The border crossing between India and Pakistan, famous for its retreat ceremony.", "estimated_time": 3.0, "approx_cost": 0, "priority": 4, "latitude": 31.6050, "longitude": 74.5739},
                    {"name": "Partition Museum", "category": "Museum", "description": "A museum housing a collection of stories, memoirs, and artifacts from the 1947 partition.", "estimated_time": 2.0, "approx_cost": 10, "priority": 4, "latitude": 31.6276, "longitude": 74.8787},
                    {"name": "Gobindgarh Fort", "category": "Fort", "description": "A historic military fort situated in the center of the city.", "estimated_time": 2.5, "approx_cost": 150, "priority": 3, "latitude": 31.6288, "longitude": 74.8621},
                ]
            },
            {
                "name": "Srinagar",
                "description": "The summer capital of Jammu and Kashmir, known for its stationary houseboats and colorful shikarhas.",
                "best_time": "April to October",
                "attractions": [
                    {"name": "Dal Lake", "category": "Lake", "description": "An urban lake, integral to tourism and recreation in Kashmir.", "estimated_time": 3.0, "approx_cost": 500, "priority": 5, "latitude": 34.1082, "longitude": 74.8601},
                    {"name": "Shalimar Bagh", "category": "Garden", "description": "A Mughal garden built by Emperor Jahangir.", "estimated_time": 2.0, "approx_cost": 25, "priority": 4, "latitude": 34.1487, "longitude": 74.8732},
                    {"name": "Shankaracharya Temple", "category": "Temple", "description": "Dedicated to Lord Shiva, located on the summit of the Shankaracharya Hill.", "estimated_time": 1.5, "approx_cost": 0, "priority": 4, "latitude": 34.0754, "longitude": 74.8496},
                    {"name": "Nishat Bagh", "category": "Garden", "description": "A terraced Mughal garden built on the eastern side of the Dal Lake.", "estimated_time": 1.5, "approx_cost": 25, "priority": 3, "latitude": 34.1246, "longitude": 74.8797},
                    {"name": "Pari Mahal", "category": "Monument", "description": "A seven terraced garden located at the top of Zabarwan mountain range.", "estimated_time": 1.5, "approx_cost": 25, "priority": 3, "latitude": 34.0864, "longitude": 74.8778},
                ]
            }
        ]

        
        # --- ADDED LOGIC FOR 10-15 ATTRACTIONS ---
        templates = [
            {"name": "{dest} Heritage Walk", "category": "Walking Tour", "description": "Explore the hidden alleys and heritage of {dest}.", "estimated_time": 2.0, "approx_cost": 0, "priority": 3},
            {"name": "{dest} Culinary Experience", "category": "Food Tour", "description": "Taste the best local street food and delicacies.", "estimated_time": 3.0, "approx_cost": 200, "priority": 4},
            {"name": "Central Museum of {dest}", "category": "Museum", "description": "Learn about the rich history and culture of the region.", "estimated_time": 2.5, "approx_cost": 50, "priority": 3},
            {"name": "{dest} Grand Bazaar", "category": "Shopping", "description": "Shop for local handicrafts, textiles, and souvenirs.", "estimated_time": 2.0, "approx_cost": 0, "priority": 4},
            {"name": "Sunset Viewpoint", "category": "Nature", "description": "Enjoy a breathtaking sunset view over {dest}.", "estimated_time": 1.5, "approx_cost": 0, "priority": 5},
            {"name": "{dest} Cultural Show", "category": "Entertainment", "description": "An evening of traditional music and dance.", "estimated_time": 2.0, "approx_cost": 300, "priority": 4},
            {"name": "Day Trip around {dest}", "category": "Tour", "description": "A comprehensive guided day tour of the outskirts.", "estimated_time": 6.0, "approx_cost": 800, "priority": 5},
        ]
        
        for dest in data:
            dest_name = dest["name"]
            # To avoid duplicates if run multiple times, only append if they have exactly 5 attractions (original seed)
            if len(dest["attractions"]) <= 5:
                base_lat = dest["attractions"][0]["latitude"] if dest["attractions"] else 0.0
                base_lng = dest["attractions"][0]["longitude"] if dest["attractions"] else 0.0
                
                for i, t in enumerate(templates):
                    new_attr = t.copy()
                    new_attr["name"] = new_attr["name"].format(dest=dest_name)
                    new_attr["description"] = new_attr["description"].format(dest=dest_name)
                    new_attr["latitude"] = base_lat + (i * 0.005)
                    new_attr["longitude"] = base_lng + (i * 0.005)
                    dest["attractions"].append(new_attr)
        # -----------------------------------------

        total_destinations = 0
        total_attractions = 0

        with transaction.atomic():
            for dest_data in data:
                destination, created = Destination.objects.get_or_create(
                    name=dest_data["name"],
                    defaults={
                        "description": dest_data["description"],
                        "best_time": dest_data["best_time"],
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created destination: {destination.name}"))
                else:
                    self.stdout.write(f"Destination {destination.name} already exists. Proceeding with attractions.")
                
                total_destinations += 1
                
                # Fetch all existing attraction names in one query (avoids N+1)
                existing_names = set(
                    Attraction.objects.filter(destination=destination)
                    .values_list("name", flat=True)
                )

                attractions_to_create = [
                    Attraction(
                        destination=destination,
                        name=attr_data["name"],
                        category=attr_data["category"],
                        description=attr_data["description"],
                        estimated_time=attr_data["estimated_time"],
                        approx_cost=attr_data["approx_cost"],
                        priority=attr_data["priority"],
                        latitude=attr_data["latitude"],
                        longitude=attr_data["longitude"],
                    )
                    for attr_data in dest_data["attractions"]
                    if attr_data["name"] not in existing_names
                ]
                
                if attractions_to_create:
                    Attraction.objects.bulk_create(attractions_to_create)
                    self.stdout.write(self.style.SUCCESS(f"  -> Added {len(attractions_to_create)} attractions for {destination.name}"))
                    total_attractions += len(attractions_to_create)

        self.stdout.write(self.style.SUCCESS(f"Successfully processed {total_destinations} destinations and added {total_attractions} new attractions."))
