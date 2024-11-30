entity={
    "pharmacy":["pharmacy","pharmaceutical","pharmaceuticals","pharmacist","pharmacists","pharmacies"],
    "hospital":["hospital","hospitals","healthcare","health care","health","care","clinic","clinics","medical","medicals","medicine","medicines"],
    "school":["school","schools","education","educational","educations","educational"],
    "college":["college","colleges"],
    "bank":["bank","banks","banking","finance","financial","finances","financials"],
    "stationery":["stationery","stationeries","book","books","bookstore","bookstores","stationery store","stationery stores"],
    "hall":["hall","halls","cinemas","cinema","theatre","theatres"],
    "hotel":["hotel","hotels","guest house","guest houses","motel","motels","inn","inns","resort","resorts","lodge","lodges"],
    "restaurant":["restaurant","restaurants","cafe","cafes","food","foods","fast food","fast foods"],
    "party venue":["party venue","party venues","party hall","party halls","party palace","party palaces","venue","venues","hall","halls","palace","palaces","banquet","banquets"],
}

def entity_classify(extracted_text):
    for text in extracted_text:
        found = False
        for key, value in entity.items():
            for v in value:
                if v in text.lower():
                    print(f"Entity: {text}, Category: {key}")
                    found = True
                    break
            if found:
                break
        if not found:
            print(f"Entity: {text}, Category: others")


if __name__=="__main__":
    extracted_text=[
        "Lainchaur Pharmacy",
        "Pacific Guest House and Apartment",
        "National School of Sciences",
        "Modern Nepal College",
        "Daksha Travel and Tours Pvt. Ltd.",
        "Nepal Bank Limited",
        "Namaste Party Venue",
        "Saraswati Books Store",
        "QFX Cinemas",
        "ABC Fast Food",
        "Kathmandu Guest House",
        "College of Medicines"

    ]
    entity_classify(extracted_text)
