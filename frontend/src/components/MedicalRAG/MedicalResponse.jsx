import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { ScrollArea } from "@/components/ui/scroll-area";

/**
 * MedicalResponse component to display the answer from the medical RAG system
 */
const MedicalResponse = ({ answer, sources }) => {
  if (!answer) return null;

  return (
    <Card className="w-full mt-4 border-blue-200 shadow-md">
      <CardHeader className="bg-blue-50">
        <CardTitle className="text-xl text-blue-700">Medical Answer</CardTitle>
        <CardDescription>Response from Bio-Mistral 7B medical model</CardDescription>
      </CardHeader>
      <CardContent className="pt-4 text-gray-800">
        <ScrollArea className="h-[200px]">
          <div className="whitespace-pre-wrap">{answer}</div>
        </ScrollArea>
      </CardContent>
      {sources && sources.length > 0 && (
        <CardFooter className="bg-gray-50 flex flex-col items-start">
          <p className="text-sm font-medium mb-2">Sources:</p>
          <Accordion type="single" collapsible className="w-full">
            {sources.map((source, index) => (
              <AccordionItem key={index} value={`source-${index}`}>
                <AccordionTrigger className="text-sm text-gray-600">
                  Source {index + 1}
                </AccordionTrigger>
                <AccordionContent>
                  <div className="text-xs bg-gray-50 p-2 rounded border">
                    {source}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </CardFooter>
      )}
    </Card>
  );
};

export default MedicalResponse;
