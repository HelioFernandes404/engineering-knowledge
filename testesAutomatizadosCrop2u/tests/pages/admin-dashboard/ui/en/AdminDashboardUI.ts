export const OverviewUsuario = {
    aprovar: 'APPROVE',
    reprovar: 'DISAPPROVE',
};

export const OverviewProposta = {
    tipoVenda: 'Sell',
    tipoCompra: 'Buy',
} as const;

export const GridPropostas = {
    status: {
        'UNDER-REVIEW': 'Under Review',
        AVAILABLE: 'Available',
        DEALING: 'Dealing',
        FINISHED: 'Suspended',
        SUSPENDED: 'Suspensa',
        CANCELED: 'Canceled',
        EXPIRED: 'Expired',
    },
} as const;
