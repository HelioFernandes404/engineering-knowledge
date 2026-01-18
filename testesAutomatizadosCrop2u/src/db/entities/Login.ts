import { ILoginEntity } from '@src/interfaces/logins';

export default class Login implements ILoginEntity {
    private id: string;
    private email: string;
    private role: string;

    constructor(dados: any) {
        this.id = dados.id ?? dados._id;
        this.email = dados.email;
        this.role = dados.role;
    }

    getEmail(): string {
        return this.email;
    }

    getRole(): string {
        return this.role;
    }

    getID(): string {
        return this.id;
    }
}
