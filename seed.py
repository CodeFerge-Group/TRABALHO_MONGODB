from pymongo import MongoClient
import random, datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_db"]

PRODUTOS = {
    "Eletronicos": [
        {"nome": "Samsung Smart TV 4K 55 Polegadas", "marca": "Samsung", "sub": "Televisoes", "preco": 299990},
        {"nome": "LG Smart TV OLED 65 Polegadas", "marca": "LG", "sub": "Televisoes", "preco": 589990},
        {"nome": "Sony Bravia 50 Full HD", "marca": "Sony", "sub": "Televisoes", "preco": 189990},
        {"nome": "Hisense TV 43 4K UHD", "marca": "Hisense", "sub": "Televisoes", "preco": 145000},
        {"nome": "iPhone 15 Pro 128GB Titanio", "marca": "Apple", "sub": "Smartphones", "preco": 459990},
        {"nome": "Samsung Galaxy S24 256GB Preto", "marca": "Samsung", "sub": "Smartphones", "preco": 389990},
        {"nome": "Huawei P60 Pro 256GB", "marca": "Huawei", "sub": "Smartphones", "preco": 299990},
        {"nome": "Xiaomi Redmi Note 13 128GB", "marca": "Xiaomi", "sub": "Smartphones", "preco": 89990},
        {"nome": "Tecno Spark 20 Pro 128GB", "marca": "Tecno", "sub": "Smartphones", "preco": 55000},
        {"nome": "Dell Inspiron 15 i7 16GB 512GB SSD", "marca": "Dell", "sub": "Computadores", "preco": 389990},
        {"nome": "HP Pavilion 14 i5 8GB 256GB SSD", "marca": "HP", "sub": "Computadores", "preco": 259990},
        {"nome": "Lenovo IdeaPad 3 Ryzen 5 8GB", "marca": "Lenovo", "sub": "Computadores", "preco": 219990},
        {"nome": "Apple MacBook Air M2 8GB 256GB", "marca": "Apple", "sub": "Computadores", "preco": 689990},
        {"nome": "Asus VivoBook 15 i3 8GB 256GB", "marca": "Asus", "sub": "Computadores", "preco": 179990},
        {"nome": "Samsung Galaxy Tab A9 64GB", "marca": "Samsung", "sub": "Tablets", "preco": 119990},
        {"nome": "Apple iPad 10 64GB WiFi", "marca": "Apple", "sub": "Tablets", "preco": 349990},
        {"nome": "Sony WH-1000XM5 Headphones", "marca": "Sony", "sub": "Audio", "preco": 189990},
        {"nome": "JBL Charge 5 Bluetooth Speaker", "marca": "JBL", "sub": "Audio", "preco": 65990},
        {"nome": "Canon EOS R50 Kit 18-45mm", "marca": "Canon", "sub": "Cameras", "preco": 459990},
        {"nome": "PlayStation 5 Slim 1TB", "marca": "Sony", "sub": "Gaming", "preco": 389990},
    ],
    "Moda": [
        {"nome": "Tenis Nike Air Max 270 Preto 42", "marca": "Nike", "sub": "Calcados", "preco": 65990},
        {"nome": "Tenis Adidas Ultraboost 22 Branco 41", "marca": "Adidas", "sub": "Calcados", "preco": 72990},
        {"nome": "Tenis Puma Suede Classic Azul 40", "marca": "Puma", "sub": "Calcados", "preco": 45990},
        {"nome": "Sapato Social Masculino Couro Preto 43", "marca": "Bata", "sub": "Calcados", "preco": 28990},
        {"nome": "Sandalia Feminina Salto Alto Dourada 38", "marca": "Arezzo", "sub": "Calcados", "preco": 22990},
        {"nome": "Chinelo Havaianas Top Azul 39", "marca": "Havaianas", "sub": "Calcados", "preco": 5990},
        {"nome": "Vestido Kitenge Estampado Midi M", "marca": "Luanda Fashion", "sub": "Vestuario", "preco": 12500},
        {"nome": "Camisa Social Slim Fit Branca M", "marca": "Zara", "sub": "Vestuario", "preco": 8990},
        {"nome": "Calca Jeans Skinny Azul Escuro 38", "marca": "Levi Strauss", "sub": "Vestuario", "preco": 15990},
        {"nome": "Blazer Feminino Alfaiataria Preto G", "marca": "Renner", "sub": "Vestuario", "preco": 18990},
        {"nome": "Vestido Longo Floral Estampado G", "marca": "H&M", "sub": "Vestuario", "preco": 14990},
        {"nome": "Camisola Capuz Nike Fleece Cinza M", "marca": "Nike", "sub": "Roupa Desportiva", "preco": 19990},
        {"nome": "Conjunto Desportivo Adidas Preto M", "marca": "Adidas", "sub": "Roupa Desportiva", "preco": 24990},
        {"nome": "Legging Compressao Under Armour Preta M", "marca": "Under Armour", "sub": "Roupa Desportiva", "preco": 16990},
        {"nome": "Casaco Impermeavel The North Face Azul L", "marca": "The North Face", "sub": "Roupa Desportiva", "preco": 45990},
        {"nome": "Camiseta Polo Ralph Lauren Branca M", "marca": "Ralph Lauren", "sub": "Vestuario", "preco": 25990},
        {"nome": "Short Bermuda Nike Dri-Fit Preto L", "marca": "Nike", "sub": "Roupa Desportiva", "preco": 12990},
        {"nome": "Tenis Vans Old Skool Preto Branco 41", "marca": "Vans", "sub": "Calcados", "preco": 38990},
        {"nome": "Bota Couro Masculina Marrom 42", "marca": "Timberland", "sub": "Calcados", "preco": 55990},
        {"nome": "Meia Adidas Performance Pack 3 Pares", "marca": "Adidas", "sub": "Vestuario", "preco": 3990},
    ],
    "Acessorios": [
        {"nome": "Relogio Casio G-Shock GA-2100 Preto", "marca": "Casio", "sub": "Relogios", "preco": 38500},
        {"nome": "Relogio Casio Edifice EFR-303 Prata", "marca": "Casio", "sub": "Relogios", "preco": 52000},
        {"nome": "Relogio Tissot T-Classic Dourado", "marca": "Tissot", "sub": "Relogios", "preco": 145000},
        {"nome": "Smartwatch Samsung Galaxy Watch 6", "marca": "Samsung", "sub": "Relogios", "preco": 89990},
        {"nome": "Apple Watch Series 9 45mm Preto", "marca": "Apple", "sub": "Relogios", "preco": 189990},
        {"nome": "Oculos Ray-Ban Aviador Dourado G15", "marca": "Ray-Ban", "sub": "Oculos", "preco": 45000},
        {"nome": "Oculos Ray-Ban Wayfarer Preto", "marca": "Ray-Ban", "sub": "Oculos", "preco": 38000},
        {"nome": "Oculos de Sol Oakley Holbrook Azul", "marca": "Oakley", "sub": "Oculos", "preco": 42000},
        {"nome": "Mala Couro Genuino Michael Kors Castanha", "marca": "Michael Kors", "sub": "Bolsas", "preco": 98000},
        {"nome": "Mala Gucci GG Marmont Mini Preta", "marca": "Gucci", "sub": "Bolsas", "preco": 450000},
        {"nome": "Mochila Nike Heritage Preta 25L", "marca": "Nike", "sub": "Bolsas", "preco": 18990},
        {"nome": "Carteira Couro Masculina Louis Vuitton", "marca": "Louis Vuitton", "sub": "Bolsas", "preco": 185000},
        {"nome": "Pulseira Ouro 18K Feminina 18cm", "marca": "Pandora", "sub": "Bijuteria", "preco": 125000},
        {"nome": "Colar Prata 925 com Pendente", "marca": "Pandora", "sub": "Bijuteria", "preco": 18500},
        {"nome": "Brinco Argola Dourada Feminino", "marca": "Swarovski", "sub": "Bijuteria", "preco": 12000},
        {"nome": "Anel Ouro 18K com Diamante", "marca": "Tiffany", "sub": "Bijuteria", "preco": 350000},
        {"nome": "Cinto Couro Masculino Preto 90cm", "marca": "Lacoste", "sub": "Bijuteria", "preco": 15000},
        {"nome": "Chapeu Fedora Palha Bege Feminino", "marca": "Zara", "sub": "Bijuteria", "preco": 8500},
        {"nome": "Lenco Seda Hermes Estampado", "marca": "Hermes", "sub": "Bijuteria", "preco": 95000},
        {"nome": "Perfume Dior Sauvage 100ml EDP", "marca": "Dior", "sub": "Bijuteria", "preco": 65000},
    ],
    "Automoveis": [
        {"nome": "Toyota Corolla Cross 2.0 Hibrido 2024", "marca": "Toyota", "sub": "Carros", "preco": 17200000},
        {"nome": "Toyota Hilux 2.8 TDI 4x4 2023", "marca": "Toyota", "sub": "Carros", "preco": 22500000},
        {"nome": "Honda Civic 1.5 Turbo 2023", "marca": "Honda", "sub": "Carros", "preco": 14800000},
        {"nome": "Hyundai Tucson 1.6 T-GDI 2024", "marca": "Hyundai", "sub": "Carros", "preco": 16500000},
        {"nome": "Kia Sportage 1.6 T-GDI 2024", "marca": "Kia", "sub": "Carros", "preco": 15900000},
        {"nome": "Ford Ranger 3.2 TDCi 4x4 2023", "marca": "Ford", "sub": "Carros", "preco": 19800000},
        {"nome": "Mitsubishi L200 Triton 2.4 2023", "marca": "Mitsubishi", "sub": "Carros", "preco": 18200000},
        {"nome": "Nissan Navara 2.3 dCi 2023", "marca": "Nissan", "sub": "Carros", "preco": 17500000},
        {"nome": "Honda CB 500F 2023 Vermelha", "marca": "Honda", "sub": "Motorizadas", "preco": 4800000},
        {"nome": "Yamaha MT-07 689cc 2023 Preta", "marca": "Yamaha", "sub": "Motorizadas", "preco": 6200000},
        {"nome": "Honda CG 160 Fan 2024 Azul", "marca": "Honda", "sub": "Motorizadas", "preco": 1250000},
        {"nome": "Yamaha Factor 150 2024 Preta", "marca": "Yamaha", "sub": "Motorizadas", "preco": 1150000},
        {"nome": "Kawasaki Ninja 400 2023 Verde", "marca": "Kawasaki", "sub": "Motorizadas", "preco": 5800000},
        {"nome": "Bicicleta Trek Marlin 5 Mountain 29", "marca": "Trek", "sub": "Bicicletas", "preco": 850000},
        {"nome": "Bicicleta Caloi Elite Carbon 2023", "marca": "Caloi", "sub": "Bicicletas", "preco": 1200000},
        {"nome": "Bicicleta Electrica Xiaomi Himo Z20", "marca": "Xiaomi", "sub": "Bicicletas", "preco": 650000},
        {"nome": "Bicicleta Infantil Aro 20 Azul", "marca": "Caloi", "sub": "Bicicletas", "preco": 85000},
        {"nome": "Camiao Mercedes Actros 2545 2022", "marca": "Mercedes", "sub": "Camioes", "preco": 85000000},
        {"nome": "Camiao Volvo FH 460 2023", "marca": "Volvo", "sub": "Camioes", "preco": 92000000},
        {"nome": "Camiao MAN TGX 18.440 2022", "marca": "MAN", "sub": "Camioes", "preco": 78000000},
    ]
}

STATUS = ["active", "active", "active", "active", "inactive"]

def classificar(estrelas):
    if estrelas == 5: return "Excelente"
    elif estrelas in [3, 4]: return "Bom"
    elif estrelas == 2: return "Medio"
    elif estrelas == 1: return "Mais ou Menos"
    else: return "Ruim"

def gerar_produto(i, categoria, produto):
    preco_orig = produto["preco"]
    desconto = random.uniform(0.80, 0.99)
    preco_atual = round(preco_orig * desconto, 0)
    total_reviews = random.randint(0, 100)
    positivas = random.randint(int(total_reviews * 0.4), total_reviews)
    negativas = total_reviews - positivas

    if total_reviews == 0:
        estrelas = 0
        classif = "Ruim"
    elif positivas > negativas:
        estrelas = 5
        classif = "Excelente"
    else:
        estrelas = random.randint(1, 3)
        classif = classificar(estrelas)

    cores = ["Preto", "Branco", "Azul", "Vermelho", "Cinza", "Dourado", "Prata"]
    tamanhos = ["XS", "S", "M", "L", "XL", "XXL"]

    return {
        "sku": f"{categoria[:3].upper()}-{produto['sub'][:3].upper()}-{i:06d}",
        "name": produto["nome"],
        "brand": produto["marca"],
        "category": categoria,
        "subcategoria": produto["sub"],
        "price": {
            "original": preco_orig,
            "current": preco_atual,
            "currency": "AOA"
        },
        "stock": {
            "qty": random.randint(0, 200),
            "warehouse": random.choice(["LDA-01", "LDA-02", "LDA-03", "LDA-AUTO"])
        },
        "attributes": {
            "cor": random.choice(cores),
            "disponivel_em": random.sample(tamanhos, k=random.randint(2, 4)),
            "garantia": f"{random.choice([6, 12, 24])} meses",
            "origem": random.choice(["Angola", "Portugal", "China", "EUA", "Japao"])
        },
        "tags": [produto["marca"].lower(), categoria.lower(), produto["sub"].lower()],
        "rating_summary": {
            "total_reviews": total_reviews,
            "positivas": positivas,
            "negativas": negativas,
            "media": round(random.uniform(3.0, 5.0) if total_reviews > 0 else 0, 1),
            "estrelas_produto": estrelas,
            "classificacao": classif
        },
        "status": random.choice(STATUS),
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    }

TOTAL = 120000
LOTE = 1000
contador = 0

categorias_lista = list(PRODUTOS.keys())
todos_produtos = []
for cat, prods in PRODUTOS.items():
    for p in prods:
        todos_produtos.append((cat, p))

print(f"Iniciando seed de {TOTAL} produtos reais...")
print("Aguarde...")

lote = []
for i in range(TOTAL):
    cat, prod = random.choice(todos_produtos)
    lote.append(gerar_produto(i, cat, prod))
    if len(lote) == LOTE:
        db.products.insert_many(lote)
        contador += LOTE
        percentagem = round((contador / TOTAL) * 100)
        print(f"  Inseridos: {contador}/{TOTAL} ({percentagem}%)")
        lote = []

total_final = db.products.count_documents({})
print(f"\nSeed concluido!")
print(f"Total na base de dados: {total_final}")
client.close()
