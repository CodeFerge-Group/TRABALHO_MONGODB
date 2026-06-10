
// TRABALHO PRATICO : SGBD II 2025/2026
// Catalogo de Produtos Dinamico :MongoDB NoSQL
// Docente: Moyo Kanivengidio
// Grupo: Antonio Almeida K. Nzinga, Kiassisua Simao Pedro,
//        Luis Mucuzo Antonio, Maria Tumba D. Joao,
//        Suzana Diasivi Nicolau

// FICHEIRO: queries.js
// Descricao: Consultas avancadas executadas na base de dados
//            ecommerce_db no MongoDB 7.0
// Como executar: docker exec -it mongo_ecommerce mongosh
//                use ecommerce_db
//                Copiar e colar cada query abaixo




// QUERY 1 :Busca com filtros multiplos e ordenacao
// Objectivo: Encontrar os 5 electronicos mais baratos
//            abaixo de 400.000 AOA com status activo,
//            ordenados por preco crescente


db.products.find({
  category: "Eletronicos",
  "price.current": { $lte: 400000 },
  status: "active"
},
{
  name: 1,
  brand: 1,
  "price.current": 1,
  "rating_summary.classificacao": 1,
  _id: 0
}).sort({ "price.current": 1 }).limit(5)



// QUERY 2 : Aggregation Pipeline por categoria
// Objectivo: Total de produtos, preco medio, minimo e maximo
//            de cada categoria, ordenados por total


db.products.aggregate([
  {
    $group: {
      _id: "$category",
      total: { $sum: 1 },
      preco_medio: { $avg: "$price.current" },
      preco_min: { $min: "$price.current" },
      preco_max: { $max: "$price.current" }
    }
  },
  { $sort: { total: -1 } }
])


// QUERY 3 : Update parcial de preco e stock
// Objectivo: Actualizar apenas o preco actual e stock
//            da Smart TV Samsung sem alterar outros campos


db.products.updateOne(
  { sku: "ELET-TV-001" },
  {
    $set: {
      "price.current": 279990,
      "stock.qty": 40,
      updated_at: new Date()
    }
  }
)



// QUERY 4 :Busca por rating e classificacao
// Objectivo: Produtos classificados como Excelente
//            com mais de 10 avaliacoes, ordenados por reviews


db.products.find(
  {
    "rating_summary.classificacao": "Excelente",
    "rating_summary.total_reviews": { $gt: 10 }
  },
  {
    name: 1,
    brand: 1,
    "rating_summary.estrelas_produto": 1,
    "rating_summary.total_reviews": 1,
    _id: 0
  }
).sort({ "rating_summary.total_reviews": -1 }).limit(10)



// QUERY 5 :$facet: analise combinada
// Objectivo: Numa unica query retorna simultaneamente
//            distribuicao por classificacao E total por categoria


db.products.aggregate([
  {
    $facet: {
      por_classificacao: [
        {
          $group: {
            _id: "$rating_summary.classificacao",
            total: { $sum: 1 }
          }
        },
        { $sort: { total: -1 } }
      ],
      por_categoria: [
        {
          $group: {
            _id: "$category",
            total: { $sum: 1 }
          }
        },
        { $sort: { total: -1 } }
      ]
    }
  }
])



// QUERY 6 :Produtos com desconto superior a 15%
// Objectivo: Calcular percentagem de desconto e filtrar
//            produtos com mais de 15% de desconto


db.products.find(
  {
    $expr: {
      $gt: [
        {
          $divide: [
            { $subtract: ["$price.original", "$price.current"] },
            "$price.original"
          ]
        },
        0.15
      ]
    }
  },
  {
    name: 1,
    brand: 1,
    "price.original": 1,
    "price.current": 1,
    _id: 0
  }
).limit(10)

// QUERY 7 :Top 5 marcas com mais stock total
// Objectivo: Somar o stock total por marca e mostrar
//            as 5 com mais unidades disponiveis


db.products.aggregate([
  { $match: { status: "active" } },
  {
    $group: {
      _id: "$brand",
      stock_total: { $sum: "$stock.qty" },
      total_produtos: { $sum: 1 }
    }
  },
  { $sort: { stock_total: -1 } },
  { $limit: 5 }
])



// QUERY 8 :Estatisticas completas por categoria
// Objectivo: Total de produtos, preco medio/min/max,
//            media de estrelas e total de reviews por categoria


db.products.aggregate([
  {
    $group: {
      _id: "$category",
      total_produtos: { $sum: 1 },
      preco_medio: { $avg: "$price.current" },
      preco_min: { $min: "$price.current" },
      preco_max: { $max: "$price.current" },
      media_estrelas: { $avg: "$rating_summary.estrelas_produto" },
      total_reviews: { $sum: "$rating_summary.total_reviews" }
    }
  },
  { $sort: { total_produtos: -1 } }
])



// INDICES CRIADOS
// Executados apos a insercao dos dados


db.products.createIndex({ category: 1, "price.current": 1 })

db.products.createIndex({ brand: 1, "rating_summary.estrelas_produto": -1 })

db.products.createIndex({ sku: 1 }, { unique: true })

db.products.createIndex({ status: 1, "stock.qty": 1 })

db.products.createIndex({
  "rating_summary.classificacao": 1,
  "rating_summary.total_reviews": -1
})

db.avaliacoes.createIndex({ product_sku: 1 })





// ANALISE DE DESEMPENHO :explain()
// Executado para medir o impacto dos indices


db.products.find({
  category: "Eletronicos",
  "price.current": { $lte: 400000 }
}).explain("executionStats")



// CONTAGEM FINAL DOS DOCUMENTOS
// Executado para confirmar o volume de dados


db.products.countDocuments()
// Resultado: 120008

db.avaliacoes.countDocuments()
// Resultado: 13

db.categories.countDocuments()
// Resultado: 4
