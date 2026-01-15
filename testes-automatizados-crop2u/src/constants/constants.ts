import { getEnv } from '@src/helpers/helpers';

// Exporta as credenciais do cliente se definidas, senão, realiza uma ação
export const EMAIL_CLIENT = getEnv('USER_CLIENT');

export const SENHA_CLIENT = getEnv('PWD_CLIENT');

export const BACKEND_BASE_URL = getEnv('BACKEND_BASE_URL');

export const UNIDADE_MEDIDA_QTD_PRODUTO = 'MT';

export const NACIONALIDADE_BR = 'BR';

export const NACIONALIDADE_RUSSA = 'RU';

// prettier-ignore
export const SIGLAS_PAISES = [
    'AF', 'ZA', 'AL', 'DE', 'AD', 'AO', 'AG', 'SA', 'DZ', 'AR', 'AM', 'AU',
    'AT', 'AZ', 'BS', 'BD', 'BB', 'BH', 'BE', 'BZ', 'BJ', 'BY', 'BO', 'BA',
    'BW', 'BR', 'BN', 'BG', 'BF', 'BI', 'BT', 'CV', 'KH', 'CM', 'CA', 'QA',
    'KZ', 'CF', 'TD', 'CZ', 'CL', 'CN', 'CY', 'CO', 'KM', 'CG', 'CD', 'KR',
    'KP', 'CI', 'CR', 'HR', 'CU', 'DK', 'DJ', 'DM', 'DO', 'EG', 'SV', 'AE',
    'EC', 'ER', 'SK', 'SI', 'ES', 'US', 'EE', 'SZ', 'ET', 'FJ', 'PH', 'FI',
    'FR', 'GA', 'GM', 'GH', 'GE', 'GD', 'GR', 'GT', 'GY', 'GW', 'GN', 'GQ',
    'HT', 'HN', 'HU', 'YE', 'IN', 'ID', 'IQ', 'IR', 'IE', 'IS', 'IL', 'IT',
    'JM', 'JP', 'JO', 'KW', 'LA', 'LS', 'LV', 'LB', 'LR', 'LY', 'LI', 'LT',
    'LU', 'MK', 'MG', 'MY', 'MW', 'MV', 'ML', 'MT', 'MA', 'MH', 'MU', 'MR',
    'MX', 'MM', 'FM', 'MZ', 'MD', 'MC', 'MN', 'ME', 'NA', 'NR', 'NP', 'NI',
    'NE', 'NG', 'NO', 'NZ', 'OM', 'NL', 'PW', 'PA', 'PG', 'PK', 'PY', 'PE',
    'PL', 'PT', 'KE', 'KG', 'KI', 'GB', 'RO', 'RW', 'RU', 'WS', 'SB', 'SM',
    'LC', 'KN', 'ST', 'VC', 'SC', 'SN', 'LK', 'SL', 'RS', 'SG', 'SY', 'SO',
    'SD', 'SS', 'SE', 'CH', 'SR', 'TH', 'TJ', 'TZ', 'TL', 'TG', 'TO', 'TT',
    'TN', 'TM', 'TR', 'TV', 'UA', 'UG', 'UY', 'UZ', 'VU', 'VE', 'VN', 'ZM',
    'ZW',
] as const;

// Exporta as credenciais do administrador se definidas, senão, realiza uma ação
//export const EMAIL_ADMIN = process.env.USER_ADMIN || handleUndefined("USER_ADMIN");
//export const SENHA_ADMIN = process.env.PWD_ADMIN || handleUndefined("PWD_ADMIN");
