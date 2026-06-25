export const pl = {
  metadata: {
    title: "PrzeczytAI.me",
    description:
      "PrzeczytAI.me zamienia zaszumione polskie dokumenty w uporządkowany tekst, SSML i gotową narrację.",
  },
  landing: {
    productName: "PrzeczytAI.me",
    valueProposition:
      "Zamieniaj dowolnie sformatowane polskie dokumenty w uporządkowany tekst i gotową narrację.",
    actions: {
      openApp: "Przejdź do dokumentów",
      signUp: "Utwórz konto",
      signIn: "Zaloguj się",
      viewDocs: "Zobacz dokumentację",
    },
    demo: {
      label: "Przykład pracy aplikacji PrzeczytAI.me",
    },
    docsCallout: {
      text: "Jakieś niejasności? Sprawdź naszą dokumentację.",
    },
    capabilities: {
      heading: "Co robi ta aplikacja?",
      description:
        "Jeden przycisk prowadzi dokument od surowego tekstu do materiału, którego można słuchać, który można czytać i który można pobrać.",
      items: {
        cleanup: {
          title: "Porządkowanie tekstu",
          description:
            "Usuwa szum z dokumentów i przygotowuje materiał do czytania na głos.",
        },
        ssml: {
          title: "Znaczniki SSML",
          description:
            "Dodaje pauzy, akcenty i strukturę potrzebną do naturalnej narracji.",
        },
        voice: {
          title: "Polski głos",
          description:
            "Generuje nagrania dopasowane do polskich dokumentów i dłuższych tekstów.",
        },
        highlighting: {
          title: "Podświetlanie",
          description:
            "Synchronizuje tekst z narracją, żeby łatwiej śledzić czytany fragment.",
        },
        downloads: {
          title: "Pobieranie plików",
          description:
            "Udostępnia gotowe wyniki do dalszej pracy poza aplikacją.",
        },
      },
    },
    supportedInputs: {
      heading: "Obsługiwane formaty",
      availableLabel: "Dostępne",
      plannedLabel: "W planach",
      items: [
        {
          extension: ".txt",
          status: "available",
        },
        {
          extension: ".md",
          status: "available",
        },
        {
          extension: ".pdf",
          status: "planned",
        },
        {
          extension: ".docx",
          status: "planned",
        },
      ],
    },
    footer: {
      copyright: "© 2026 PrzeczytAI.me",
      contactLabel: "Kontakt:",
      contactEmail: "informaks23@gmail.com",
    },
  },
} as const;
