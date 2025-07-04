import React from 'react';
import MedicalRAG from '@/pages/MedicalRAG';

export const metadata = {
  title: 'Medical RAG | NoteThat',
  description: 'Medical information retrieval powered by Bio-Mistral 7B',
};

export default function MedicalRAGPage() {
  return <MedicalRAG />;
}
