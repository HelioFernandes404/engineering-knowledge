import { logErro } from '@src/helpers/helpers';

export function handleUndefined(variableName: string) {
	logErro(`A variável de ambiente ${variableName} não está definida.`);
	// Lógica adicional, como lançar um erro ou tomar medidas apropriadas
	// Você pode retornar um valor padrão ou undefined, dependendo do seu caso
	return `A variável de ambiente ${variableName} não está definida.`;
}
