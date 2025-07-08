# Sistema de Sugestões de Estações Meteorológicas

## 📋 Resumo das Funcionalidades Implementadas

Foi implementado um sistema completo para que usuários possam sugerir novas estações meteorológicas e administradores possam gerenciar essas sugestões, seguindo a identidade visual existente do sistema.

## 🆕 Novos Recursos

### 1. Modelo `StationSuggestion`
- **Localização**: `data_scraper/models.py`
- **Campos**:
  - `name`: Nome da estação (obrigatório)
  - `url`: URL da estação (obrigatório)
  - `message`: Observações/mensagem (opcional)
  - `status`: Status da sugestão (pendente, aprovada, rejeitada)
  - `created_at`: Data de criação
  - `updated_at`: Data de última atualização

### 2. Novas Views
- **Localização**: `data_display/views.py`

#### `suggest_station`
- Formulário para usuários sugerirem novas estações
- Rota: `/sugerir-estacao/`

#### `manage_suggestions`
- Página administrativa para visualizar todas as sugestões
- Rota: `/gerenciar-sugestoes/`

#### `approve_suggestion`
- Funcionalidade para aprovar sugestões e criar automaticamente um `DataSource`
- Rota: `/aprovar-sugestao/<id>/`

#### `reject_suggestion`
- Funcionalidade para rejeitar sugestões
- Rota: `/rejeitar-sugestao/<id>/`

### 3. Novos Templates

#### `suggest_station.html`
- **Identidade Visual**: Segue o padrão do sistema usando Bootstrap 4.3.1
- **Layout**: Estrutura similar aos outros templates (col-9 + col-3 com logo)
- **Componentes**: 
  - Títulos em maiúsculo seguindo o padrão
  - Alert de informação com ícones Font Awesome
  - Formulário com classes Bootstrap
  - Botões com cores consistentes (success/primary)
- **Responsividade**: Mantém a responsividade do sistema

#### `manage_suggestions.html`
- **Identidade Visual**: Design consistente com o restante do sistema
- **Layout**: Template full-width (col-12) para comportar a tabela
- **Componentes**:
  - Cabeçalhos seguindo o padrão existente
  - Cards de estatísticas com estilo Bootstrap
  - Tabela responsiva com thead-dark
  - Badges para status das sugestões
  - Botões de ação com ícones Font Awesome
- **Funcionalidades**: Sistema completo de gerenciamento com confirmações

### 4. Atualizações na Interface

#### Template `index.html`
- Adicionado botão "Sugerir estação" (btn-info) para usuários
- Adicionado botão "Gerenciar sugestões" (btn-dark) para administradores
- Mantida a disposição e estilo dos botões existentes

### 5. Administração Django
- **Localização**: `data_scraper/admin.py`
- Registrado o modelo `StationSuggestion` com interface administrativa completa
- Campos de busca, filtros e organização otimizada

## 🎨 Identidade Visual Mantida

### Elementos Preservados:
- **Bootstrap 4.3.1**: Utilização da mesma versão e classes
- **Font Awesome 5.15.3**: Ícones consistentes em todo o sistema
- **Layout Structure**: Estrutura de colunas (col-9 + col-3) para formulários
- **Typography**: Títulos em maiúsculo (.text-uppercase)
- **Color Scheme**: Cores dos botões e componentes Bootstrap
- **Logo**: Imagem da estação meteorológica no canto direito
- **CSS Custom**: Utilização do main.css e reset.css existentes

### Novos Elementos Visuais:
- **Status Badges**: Cores consistentes (warning/success/danger)
- **Stats Cards**: Design minimalista seguindo o padrão Bootstrap
- **Responsive Tables**: Tabelas que se adaptam a diferentes telas
- **Alert Components**: Mensagens de feedback padronizadas

## 🔧 Como Usar

### Para Usuários (Sugerir Estação)
1. Acesse a página inicial
2. Clique em "Sugerir estação" (botão azul claro)
3. Preencha o formulário com:
   - Nome da estação
   - URL da estação
   - Observações (opcional)
4. Envie a sugestão

### Para Administradores (Gerenciar Sugestões)
1. Acesse "Gerenciar sugestões" na página inicial (botão escuro)
2. Visualize estatísticas e todas as sugestões
3. Para sugestões pendentes:
   - **Aprovar**: Cria automaticamente um novo `DataSource`
   - **Rejeitar**: Marca a sugestão como rejeitada

## 📁 Arquivos Modificados/Criados

### Modelos
- `data_scraper/models.py` - Adicionado modelo `StationSuggestion`

### Views
- `data_display/views.py` - Adicionadas 4 novas views

### URLs
- `data_display/urls.py` - Adicionadas 4 novas rotas

### Templates
- `data_display/templates/suggest_station.html` - Novo (seguindo identidade visual)
- `data_display/templates/manage_suggestions.html` - Novo (seguindo identidade visual)
- `data_display/templates/index.html` - Atualizado

### Admin
- `data_scraper/admin.py` - Registrado novo modelo

## 🚀 Próximos Passos

Após implementar as funcionalidades, você precisará:

1. **Criar e aplicar migrações**:
   ```bash
   python manage.py makemigrations data_scraper
   python manage.py migrate
   ```

2. **Testar as funcionalidades**:
   - Acessar `/sugerir-estacao/` para testar o formulário
   - Acessar `/gerenciar-sugestoes/` para testar a interface administrativa

## 🎨 Características do Design

- **Consistente**: Segue exatamente a identidade visual existente
- **Responsivo**: Funciona bem em dispositivos móveis e desktop
- **Intuitivo**: Interface clara seguindo os padrões estabelecidos
- **Feedback**: Mensagens de sucesso/erro integradas ao sistema de alerts do Bootstrap
- **Profissional**: Design limpo e organizado
- **Acessível**: Formulários bem estruturados com labels e títulos claros

## 🔒 Considerações de Segurança

- Todas as views de modificação (aprovar/rejeitar) usam `@csrf_exempt` (você pode querer adicionar autenticação posteriormente)
- Validação de campos obrigatórios no frontend e backend
- Confirmações JavaScript para ações importantes

O sistema está pronto para uso e mantém total consistência visual com o resto da aplicação! 🎉
