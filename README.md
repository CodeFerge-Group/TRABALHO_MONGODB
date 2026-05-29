Trabalho Prático — SGBD II 2025/2026
 Catálogo de Produtos Dinâmico com MongoDB (NoSQL)

Disciplina: Sistemas de Gestão de Bases de Dados II  
Docente: Moyo Kanivengidio  
Ano Lectivo: 2025/2026  

CodeForge_Group:
- António Almeida K. Nzinga
- Kiassisua Simão Pedro
- Luís Mucuzo António
- Maria Tumba D. João
- Suzana Diasivi Nicolau



 O que vai encontrar neste repositório


ecommerce-nosql/
├── README.md                               
├── relatorio/
│   └── RELATORIO_MONGODB.pdf    
├── docker-compose.yml                      
├── scripts/
│   ├── seed.py                             
│   └── queries.js                          
└── database_backup/
    └── ecommerce_db/
        ├── products.bson                   
        ├── avaliacoes.bson                 
        └── categories.bson                 




 PRÉ-REQUISITOS

Antes de começar, instale:

- Docker Desktop, não esqueçq de instalar o wsle integrar  e no powershell, instalar o kali-linux  → https://www.docker.com/products/docker-desktop/
- MongoDB Compass → https://www.mongodb.com/try/download/compass (opcional, para ver visualmente)



PASSO 1 — Clonar o repositório

Abra o terminal e execute:

digite:

git clone "link do repositorio"
cd ecommerce-nosql




 PASSO 2 — Iniciar o MongoDB com Docker

digite:

docker-compose up -d


Aguarde até ver:

✔ Container mongo_ecommerce  Started


Confirme que está a correr:
digite:

docker ps
Deve aparecer `mongo_ecommerce` com status Up.



 PASSO 3 — Importar a Base de Dados

Este comando restaura os 120.025 documentos do backup:


docker cp database_backup/ecommerce_db mongo_ecommerce:/tmp/restore_db

docker exec mongo_ecommerce mongorestore --db ecommerce_db /tmp/restore_db




 PASSO 4 — Verificar a Importação

Entre no mongosh:


docker exec -it mongo_ecommerce mongosh


Dentro do mongosh execute:

digite:

use ecommerce_db

db.products.countDocuments()

Resultado esperado: 120008

```js
db.avaliacoes.countDocuments()
```
Resultado esperado: 13

```js
db.categories.countDocuments()
```
Resultado esperado: 4



 PASSO 5 — Ver os 8 Produtos Manuais Reais

```js
db.products.find({ sku: { $in: [
  "ELET-TV-001", "ELET-CEL-002", "MODA-TEN-001", "MODA-VES-002",
  "ACES-REL-001", "ACES-BOL-002", "AUTO-CAR-001", "AUTO-MOT-002"
]}})
```

Estes 8 produtos foram inseridos manualmente :
- Smart TV 4K 55" Samsung
- iPhone 15 Pro 128GB
- Ténis Nike Air Max 270
- Vestido Kitenge Estampado
- Relógio Casio G-Shock
- Mala Couro Michael Kors
- Toyota Corolla Cross 2024
- Honda CB 500F 2023



PASSO 6 — Ver as 13 Avaliações dos Clientes

```js
db.avaliacoes.find({}, {
  "cliente.nome":1, produto_nome:1,
  estrelas:1, classificacao:1,
  comentario:1, positivo:1, _id:0
})
```

As avaliações incluem clientes como: Suzana Diasivi Nicolau, Maria Tumba D. João, António Almeida K. Nzinga, Kiassisua Simão Pedro, Luís Mucuzo António e Engenheiro Moyo.

Sistema de classificação:
- 5 estrelas = Excelente
- 3 ou 4 estrelas = Bom
- 2 estrelas = Médio
- 1 estrela = Mais ou Menos
- Sem avaliação = Ruim
- Se positivas > negativas → produto recebe 5 estrelas



PASSO 7 — Ver as 4 Categorias

```js
db.categories.find({}, { name:1, subcategorias:1, _id:0 })
```

**Resultado esperado:**
- Electrónicos → Televisões, Smartphones, Computadores
- Moda → Calçados, Vestuário, Roupa Desportiva
- Acessórios → Relógios, Óculos, Bolsas, Bijuteria
- Automóveis → Carros, Motorizadas, Bicicletas, Camiões


PASSO 8 — Executar as 8 Queries Avançadas

Query 1 — Busca filtrada com ordenação
*5 electrónicos mais baratos abaixo de 400.000 AOA, activos, ordenados por preço*
```js
db.products.find({
  category: "Eletronicos",
  "price.current": { $lte: 400000 },
  status: "active"
}, {
  name:1, brand:1, "price.current":1,
  "rating_summary.classificacao":1, _id:0
}).sort({ "price.current": 1 }).limit(5)
```



Query 2 — Aggregation Pipeline por categoria
*Total de produtos, preço médio, mínimo e máximo por categoria*
```js
db.products.aggregate([
  { $group: {
    _id: "$category",
    total: { $sum: 1 },
    preco_medio: { $avg: "$price.current" },
    preco_min: { $min: "$price.current" },
    preco_max: { $max: "$price.current" }
  }},
  { $sort: { total: -1 } }
])
```



 Query 3 — Update parcial de preço e stock
*Actualiza apenas preço e stock sem tocar nos outros campos*
```js
db.products.updateOne(
  { sku: "ELET-TV-001" },
  { $set: {
    "price.current": 279990,
    "stock.qty": 40,
    updated_at: new Date()
  }}
)
```



 Query 4 — Busca por rating e classificação
*Produtos Excelente com mais de 10 avaliações, ordenados por reviews*
```js
db.products.find({
  "rating_summary.classificacao": "Excelente",
  "rating_summary.total_reviews": { $gt: 10 }
}, {
  name:1, brand:1,
  "rating_summary.estrelas_produto":1,
  "rating_summary.total_reviews":1, _id:0
}).sort({ "rating_summary.total_reviews": -1 }).limit(10)
```



 Query 5 — $facet: análise combinada
*Numa query: distribuição por classificação E total por categoria*
```js
db.products.aggregate([{ $facet: {
  por_classificacao: [
    { $group: { _id: "$rating_summary.classificacao", total: { $sum: 1 } } },
    { $sort: { total: -1 } }
  ],
  por_categoria: [
    { $group: { _id: "$category", total: { $sum: 1 } } },
    { $sort: { total: -1 } }
  ]
}}])
```


Query 6 — Produtos com desconto superior a 15%
*Calcula percentagem de desconto e filtra produtos com mais de 15%*
```js
db.products.find({
  $expr: { $gt: [
    { $divide: [
      { $subtract: ["$price.original", "$price.current"] },
      "$price.original"
    ]},
    0.15
  ]}
}, { name:1, brand:1, "price.original":1, "price.current":1, _id:0 }
).limit(10)
```



 Query 7 — Top 5 marcas com mais stock
*Soma stock total por marca e mostra as 5 com mais unidades*
```js
db.products.aggregate([
  { $match: { status: "active" } },
  { $group: {
    _id: "$brand",
    stock_total: { $sum: "$stock.qty" },
    total_produtos: { $sum: 1 }
  }},
  { $sort: { stock_total: -1 } },
  { $limit: 5 }
])
```



 Query 8 — Estatísticas completas por categoria
*Total, preço médio/mín/máx, média de estrelas e total de reviews*
```js
db.products.aggregate([{ $group: {
  _id: "$category",
  total_produtos: { $sum: 1 },
  preco_medio: { $avg: "$price.current" },
  preco_min: { $min: "$price.current" },
  preco_max: { $max: "$price.current" },
  media_estrelas: { $avg: "$rating_summary.estrelas_produto" },
  total_reviews: { $sum: "$rating_summary.total_reviews" }
}}, { $sort: { total_produtos: -1 } }])
```



PASSO 9 — Verificar os 6 Índices Criados

```js
db.products.getIndexes()
```

Índices esperados:

| Nome | Tipo |
|------|------|
| `_id_` | UNIQUE |
| `category_1_price.current_1` | COMPOUND |
| `brand_1_rating_summary.estrelas_produto_-1` | COMPOUND |
| `sku_1` | UNIQUE |
| `status_1_stock.qty_1` | COMPOUND |
| `rating_summary.classificacao_1_rating_summary.total_reviews_-1` | COMPOUND |



PASSO 10 — Testar a Performance com explain()

```js
db.products.find({
  category: "Eletronicos",
  "price.current": { $lte: 400000 }
}).explain("executionStats")
```

Resultados obtidos pelo grupo:
- `executionTimeMillis`: 10 ms
- `stage`: IXSCAN(usou índice — não COLLSCAN)
- `indexName`: category_1_price.current_1
- `docsExamined`: 25.184
- `nReturned`: 25.184 (100% de eficiência)
- `seeks`: 1 (acesso directo ao índice)



PASSO 11 — Visualizar no MongoDB Compass (opcional)

1. Abra o MongoDB Compass
2. Clique em New Connection
3. URI: `mongodb://localhost:27017`
4. Nome: `ecommerce_docker`
5. Clique Save & Connect
6. Navegue: `ecommerce_docker` → `ecommerce_db` → `products`

No Compass pode ver:
- Documents — os 120.008 produtos
- Aggregations — construir e testar pipelines
- Schema — estrutura visual dos documentos
- Indexes — os 6 índices com estado READY
- Validation — regras de validação geradas automaticamente



Resumo do que foi implementado

| Item | Detalhe |
|------|---------|
| SGBD | MongoDB 7.0 em Docker |
| Base de dados | ecommerce_db |
| Colecções | products, avaliacoes, categories |
| Total de documentos | 120.025 |
| Produtos manuais | 8 produtos reais com atributos detalhados |
| Produtos automáticos | 120.000 gerados com script Python |
| Avaliações | 13 com nomes reais angolanos |
| Categorias | 4 (Electrónicos, Moda, Acessórios, Automóveis) |
| Queries avançadas | 8 |
| Índices criados | 6 (5 COMPOUND + 1 UNIQUE) |
| Performance medida | 10ms com 100% eficiência de índice |



Parar o ambiente

digite:

docker-compose down




*Trabalho prático desenvolvido para a disciplina SGBD II — Ano lectivo 2025/2026*
