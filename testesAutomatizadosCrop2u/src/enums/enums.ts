export enum HttpStatus {
    ServerError = 500,
    Conflitct = 409,
    NotFound = 404,
    NotAuthorized = 403,
    NotAuthenticated = 401,
    InvalidRequest = 400,
    Redirect = 303,
    Created = 201,
    Success = 200,
}

export enum TipoDocumentoEstrangeiro {
    TaxID = 1,
    NIF = 2,
    Vat = 3,
    EORI = 4,
}

export enum StatusAprovacaoUsuario {
    Reprovado,
    Aprovado,
    Pendente,
}

export enum TipoDeProposta {
    Venda = 1,
    Compra = 2,
}

export enum StatusProposta {
    Analise,
    Aberto,
    Negociacao,
    Finalizada,
    Suspensa,
    Cancelada,
    Expirada,
    Reprovada,
}

export enum Incoterms {
    EXW = 1,
    FCA = 2,
    FAS = 3,
    FOB = 4,
    CPT = 5,
    CIP = 6,
    CFR = 7,
    CIF = 8,
    DAP = 9,
    DPU = 10,
    DDP = 11,
}

export enum StatusNegociacao {
    Analise = 2,
    EmNegociacao = 1, // Ordenação por status prioriza 'EmNegociacao'
    Negociada = 3,
    Cancelada = 4,
}

export enum Role {
    usuario = 'Usuario', // Nome da coleção de usuários
    admin = 'Admin', // Nome da coleção de admins
}
