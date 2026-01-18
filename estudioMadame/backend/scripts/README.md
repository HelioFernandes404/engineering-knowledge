# Scripts de Teste - Estúdio Madame

## Seed de Dados de Teste

### `seed_test_data.py`

Script para popular o banco de dados com usuários e dados de teste completos.

#### Como Executar

```bash
cd /home/helio/Work/HelioFernandes404/estudio_madame/backend
source .venv/bin/activate
python -m scripts.seed_test_data
```

#### Dados Criados

**1 Admin:**
- Email: `teste@estudiomadame.com`
- Senha: `teste123`
- Role: `admin`

**4 Clientes:**
| Nome | Email | Senha |
|------|-------|-------|
| Maria Silva | maria.silva@email.com | cliente123 |
| João Santos | joao.santos@email.com | cliente123 |
| Ana Costa | ana.costa@email.com | cliente123 |
| Pedro Oliveira | pedro.oliveira@email.com | cliente123 |

**5 Galerias:**
- Casamento Maria & José (publicada)
- Ensaio Família Santos (em seleção pelo cliente)
- Aniversário 15 Anos Ana (rascunho)
- Ensaio Gestante (arquivada)
- Formatura Medicina (publicada)

**31 Fotos** distribuídas entre as galerias

**3 Approvals** em diferentes estados (awaiting, complete)

#### Features Testáveis

✅ Gallery Management (criar, editar, publicar)
✅ Photo Management (visualizar, selecionar)
✅ Client Management (CRUD completo)
✅ Approval Workflow (seleção e aprovação)
✅ Dashboard com estatísticas
✅ Autenticação JWT (admin e client)
✅ Privacy settings (public, private, password)

❌ Google Drive (desabilitado - a ser implementado no futuro)

#### Observações

- O script **limpa todos os dados existentes** antes de criar os novos
- As fotos usam URLs do Unsplash como placeholder
- O campo `google_drive_file_id` usa IDs falsos (prefixo `FAKE_`)
- Para preservar dados existentes, comente a linha `clear_existing_data(db)` no script

#### Próximos Passos

1. Acesse: http://localhost:5173
2. Login com `teste@estudiomadame.com` / `teste123`
3. Explore todas as funcionalidades!
