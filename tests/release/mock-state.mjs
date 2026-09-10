// The tested update contract replaces configuration; fileId alone is retained if omitted.
export function updateDraftState(previous, args) {
  return { draftId: previous.draftId, status: 'draft', fileId: previous.fileId, ...args };
}
