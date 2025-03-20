meu_projeto/
│
├── src/
│   ├── core/                     # Camada de domínio (independente de frameworks)
│   │   ├── entities/             # Entidades do domínio
│   │   ├── use_cases/             # Casos de uso (regras de negócio)
│   │   ├── repositories/          # Interfaces para repositórios
│   │   └── exceptions/           # Exceções específicas do domínio
│   │
│   ├── application/              # Camada de aplicação (orquestração de casos de uso)
│   │   ├── services/             # Serviços que coordenam casos de uso
│   │   └── dtos/                 # Objetos de transferência de dados (DTOs)
│   │
│   ├── infrastructure/           # Camada de infraestrutura (detalhes de implementação)
│   │   ├── repositories/         # Implementações concretas de repositórios
│   │   ├── database/             # Configurações e modelos de banco de dados
│   │   ├── http/                 # Controllers, rotas, etc. (se usar um framework web)
│   │   └── external_services/    # Integrações com serviços externos
│   │
│   └── presentation/             # Camada de apresentação (interfaces de usuário ou APIs)
│       ├── controllers/          # Controladores para APIs ou interfaces
│       ├── serializers/          # Serializadores para formatar dados de saída
│       └── views/                # Views (se for uma aplicação web)
│
├── tests/                        # Testes automatizados
│   ├── unit/                     # Testes unitários
│   ├── integration/              # Testes de integração
│   └── e2e/                      # Testes end-to-end
│
├── config/                       # Configurações do projeto
│   ├── settings.py               # Configurações gerais
│   └── database.py               # Configurações de banco de dados
│
├── scripts/                      # Scripts utilitários (ex.: migrações, seeds)
│
└── main.py                       # Ponto de entrada da aplicação
