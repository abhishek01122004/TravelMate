from django.shortcuts import get_object_or_404, render

from .models import Destination

# Fallback hero images when no upload is stored (Unsplash CDN)
_DEFAULT_COVER = (
    "https://images.unsplash.com/photo-1488646953014-85cb44e25828"
    "?auto=format&fit=crop&w=1200&q=80"
)
_COVER_BY_NAME = {
    "goa": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/BeachFun.jpg/3840px-BeachFun.jpg",
    "jaipur": "https://upload.wikimedia.org/wikipedia/commons/4/41/East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg",
    "agra": "https://upload.wikimedia.org/wikipedia/commons/6/68/Taj_Mahal%2C_Agra%2C_India.jpg",
    "mumbai": "https://upload.wikimedia.org/wikipedia/commons/2/2b/Mumbai_Bandra-Worli_Sea_Link.jpg",
    "delhi": "https://upload.wikimedia.org/wikipedia/commons/4/40/Jama_Masjid_2011.jpg",
    "varanasi": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Varanasi%2C_India%2C_Ghats%2C_Cremation_ceremony_in_progress.jpg",
    "udaipur": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Evening_view%2C_City_Palace%2C_Udaipur.jpg",
    "munnar": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Munnar_Overview.jpg/3840px-Munnar_Overview.jpg",
    "leh": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Leh_City_seen_from_Shanti_Stupa.JPG/3840px-Leh_City_seen_from_Shanti_Stupa.JPG",
    "darjeeling": "https://upload.wikimedia.org/wikipedia/commons/9/96/DarjeelingTrainFruitshop_%282%29.jpg",
    "port blair": "https://upload.wikimedia.org/wikipedia/commons/9/9b/View_from_South_Point%2C_%28Port_Blair%2C_India%29.jpg",
    "shimla": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Landscape_of_Shimla_%2C_Himachal_Pradesh.jpg/3840px-Landscape_of_Shimla_%2C_Himachal_Pradesh.jpg",
    "ooty": "https://upload.wikimedia.org/wikipedia/commons/d/db/Ooty_lake.jpg",
    "jaisalmer": "https://upload.wikimedia.org/wikipedia/commons/4/46/Jaisalmer_Fort.jpg",
    "rishikesh": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Trayambakeshwar_Temple_VK.jpg/3840px-Trayambakeshwar_Temple_VK.jpg",
    "hampi": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Wide_angle_of_Galigopuram_of_Virupaksha_Temple%2C_Hampi_%2804%29_%28cropped%29.jpg/3840px-Wide_angle_of_Galigopuram_of_Virupaksha_Temple%2C_Hampi_%2804%29_%28cropped%29.jpg",
    "mysore": "https://upload.wikimedia.org/wikipedia/commons/5/56/Mysuru_Montage.jpg",
    "kolkata": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Kolkata_maidan.jpg",
    "hyderabad": "https://upload.wikimedia.org/wikipedia/commons/8/88/Downtown_hyderabad_drone.png",
    "chennai": "https://upload.wikimedia.org/wikipedia/commons/3/32/Chennai_Central.jpg",
    "bangalore": "https://upload.wikimedia.org/wikipedia/commons/c/cd/View_from_Visvesvaraya_Industrial_and_Technological_Museum_%282025%29_02.jpg",
    "pune": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Pune_West_skyline_-_March_2017.jpg/3840px-Pune_West_skyline_-_March_2017.jpg",
    "amritsar": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Golden_Temple_Amritsar_Gurudwara_%28cropped%29.jpg",
    "srinagar": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Red_and_Yellow_Tulips.JPG",
    "manali": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80",
}


def _legacy_cover_url(destination):
    name_key = (destination.name or "").strip().lower()
    if name_key in _COVER_BY_NAME:
        return _COVER_BY_NAME[name_key]
    
    # Generate a unique, consistent image for each destination using a seed
    return f"https://picsum.photos/seed/dest_{destination.pk}/1200/800"


def display_cover_url(destination):
    """Prefer uploaded cover_image; otherwise name/PK-based Unsplash fallback."""
    if getattr(destination, "cover_image", None) and destination.cover_image.name:
        if destination.cover_image.name.startswith("http"):
            return destination.cover_image.name
        return destination.cover_image.url
    return _legacy_cover_url(destination)


def destination_list(request):
    destinations = list(Destination.objects.all().order_by("name"))
    for d in destinations:
        d.display_cover_url = display_cover_url(d)
    context = {"destinations": destinations}
    return render(request, "destinations/list.html", context)


def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    destination.display_cover_url = display_cover_url(destination)
    attractions = destination.attractions.all().order_by("name")
    context = {"destination": destination, "attractions": attractions}
    return render(request, "destinations/detail.html", context)
