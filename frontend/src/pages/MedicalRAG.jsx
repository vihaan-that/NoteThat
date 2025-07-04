import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { AlertCircle } from "lucide-react";

import MedicalSearchBar from '@/components/MedicalRAG/MedicalSearchBar';
import MedicalResponse from '@/components/MedicalRAG/MedicalResponse';
import DocumentUpload from '@/components/MedicalRAG/DocumentUpload';
import { queryMedicalRAG, checkHealth } from '@/services/medicalRagService';

/**
 * MedicalRAG page that integrates all the medical RAG components
 */
const MedicalRAG = () => {
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [systemStatus, setSystemStatus] = useState({ healthy: false, loading: true });

  // Check system health on component mount
  useEffect(() => {
    const checkSystemHealth = async () => {
      try {
        const healthData = await checkHealth();
        setSystemStatus({ 
          healthy: healthData.status === 'healthy', 
          loading: false,
          details: healthData
        });
      } catch (error) {
        console.error('Error checking system health:', error);
        setSystemStatus({ 
          healthy: false, 
          loading: false,
          error: error.message 
        });
      }
    };

    checkSystemHealth();
  }, []);

  const handleSearch = async (query) => {
    setIsSearching(true);
    setAnswer('');
    setSources([]);
    
    try {
      const result = await queryMedicalRAG(query);
      setAnswer(result.answer);
      setSources(result.sources);
    } catch (error) {
      toast.error(`Search failed: ${error.message}`);
      console.error('Error searching:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleUploadComplete = () => {
    // Optionally refresh any data that needs updating after upload
    toast.info("Document indexed and ready for search");
  };

  return (
    <div className="container mx-auto py-6 max-w-4xl">
      <div className="flex flex-col gap-6">
        <div className="flex flex-col">
          <h1 className="text-3xl font-bold tracking-tight">Medical RAG System</h1>
          <p className="text-gray-500 mt-2">
            Powered by Bio-Mistral 7B and PubMedBERT for accurate medical information retrieval
          </p>
        </div>

        {!systemStatus.loading && !systemStatus.healthy && (
          <Card className="border-red-300 bg-red-50">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 text-red-700">
                <AlertCircle className="h-5 w-5" />
                <p>System unavailable: Backend API not connected</p>
              </div>
              <p className="text-sm mt-2 text-red-600">
                Please ensure the backend services are running and try again.
              </p>
              <Button
                variant="outline"
                className="mt-4 border-red-300 text-red-700"
                onClick={() => window.location.reload()}
              >
                Retry Connection
              </Button>
            </CardContent>
          </Card>
        )}

        <Tabs defaultValue="search" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="search">Search Medical Knowledge</TabsTrigger>
            <TabsTrigger value="upload">Upload Documents</TabsTrigger>
          </TabsList>
          
          <TabsContent value="search">
            <Card>
              <CardHeader>
                <CardTitle>Ask Medical Questions</CardTitle>
              </CardHeader>
              <CardContent>
                <MedicalSearchBar 
                  onSearch={handleSearch}
                  isLoading={isSearching}
                />
                
                <div className="mt-6">
                  {isSearching ? (
                    <div className="flex justify-center p-8">
                      <div className="animate-pulse text-center">
                        <p className="text-gray-500">Searching medical knowledge...</p>
                      </div>
                    </div>
                  ) : answer ? (
                    <MedicalResponse answer={answer} sources={sources} />
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <p>Ask a medical question to get started</p>
                      <p className="text-sm mt-2">Example: "What are the symptoms of Type 2 diabetes?"</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="upload">
            <DocumentUpload onUploadComplete={handleUploadComplete} />
          </TabsContent>
        </Tabs>
        
        <div>
          <Separator className="my-4" />
          <p className="text-xs text-gray-500 text-center">
            Medical information provided by Bio-Mistral 7B LLM. Consult healthcare professionals for medical advice.
          </p>
        </div>
      </div>
    </div>
  );
};

export default MedicalRAG;
