---
name: "✨ Nova Feature"
about: "Proponha um novo recurso ou melhoria para o projeto"
title: "[FEAT] "
labels: ["feature"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        # 🧩 Título
        Resuma a feature em uma linha.

  - type: input
    id: titulo
    attributes:
      label: "Título resumido"
      placeholder: "Ex: ✨ Feature: Permitir importar projetos CSV"
    validations:
      required: true

  - type: textarea
    id: resumo
    attributes:
      label: "🧭 Resumo"
      description: "Descreva em poucas linhas o que é esta feature e por que ela é importante."
      placeholder: "Resumo breve da proposta..."
    validations:
      required: true

  - type: textarea
    id: objetivo
    attributes:
      label: "🎯 Objetivo"
      description: "Explique o que se espera alcançar com esta feature."
      placeholder: "Objetivo principal da feature..."
    validations:
      required: true

  - type: checkboxes
    id: criterios
    attributes:
      label: "✅ Critérios de Aceitação"
      description: "Liste critérios claros e verificáveis para considerar a issue pronta."
      options:
        - label: "Critério 1"
        - label: "Critério 2"
        - label: "Critério 3"

  - type: checkboxes
    id: tarefas
    attributes:
      label: "🛠️ Tarefas"
      description: "Checklist para acompanhar o progresso da feature."
      options:
        - label: "Planejar"
        - label: "Implementar"
        - label: "Testar"
        - label: "Revisão de código"
        - label: "Documentação / Atualizar README"
        - label: "Deploy"

  - type: textarea
    id: detalhes
    attributes:
      label: "🧩 Detalhes / Especificações"
      description: "Descreva fluxos, endpoints, modelos de dados, mockups ou requisitos técnicos."
      placeholder: "Detalhes técnicos, endpoints, modelos, etc."

  - type: textarea
    id: ui_ux
    attributes:
      label: "🎨 UI / UX (se aplicável)"
      description: "Inclua imagens, links para Figma ou descreva interações da interface."
      placeholder: "Links, capturas ou descrição da interface..."

  - type: textarea
    id: links
    attributes:
      label: "📎 Links Úteis"
      description: "Inclua documentos, PRs ou issues relacionadas."
      placeholder: |
        - Documento / especificação:
        - PRs/Issues relacionadas:
        - Design (Figma/Zeplin):

  - type: input
    id: responsaveis
    attributes:
      label: "👥 Responsáveis"
      description: "Sugira quem pode assumir esta issue."
      placeholder: "Ex: @murilofontes, @colaborador"

  - type: textarea
    id: notas
    attributes:
      label: "🧠 Notas Técnicas / Considerações"
      description: "Observações sobre arquitetura, dependências ou riscos."
      placeholder: "Anotações técnicas importantes..."
