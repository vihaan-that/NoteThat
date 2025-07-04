import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Upload, FileText } from "lucide-react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";

/**
 * DocumentUpload component for uploading medical documents to the RAG system
 */
const DocumentUpload = ({ onUploadComplete }) => {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      // Set default title to filename without extension
      const fileNameWithoutExt = selectedFile.name.split('.').slice(0, -1).join('.');
      setTitle(fileNameWithoutExt || selectedFile.name);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file || !title.trim()) {
      toast.error("Please select a file and provide a title");
      return;
    }

    setIsUploading(true);
    
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("title", title);
      formData.append("source_type", "upload");

      const response = await fetch('http://localhost:8000/api/documents', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed with status: ${response.status}`);
      }

      const result = await response.json();
      toast.success(`Document uploaded successfully with ${result.chunks} chunks`);
      
      // Reset form
      setFile(null);
      setTitle('');
      
      // Notify parent component
      if (onUploadComplete) {
        onUploadComplete();
      }
    } catch (error) {
      toast.error(`Upload failed: ${error.message}`);
      console.error("Error uploading document:", error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-lg">Upload Medical Document</CardTitle>
        <CardDescription>
          Upload medical documents to enhance the knowledge of the RAG system
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <div className="grid w-full gap-1.5">
            <Label htmlFor="document-title">Document Title</Label>
            <Input
              id="document-title"
              type="text"
              placeholder="Enter document title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          
          <div className="grid w-full gap-1.5">
            <Label htmlFor="document-file">Document File</Label>
            <div className="flex items-center gap-2">
              <Input
                id="document-file"
                type="file"
                onChange={handleFileChange}
                accept=".txt,.pdf,.docx,.md"
                className="file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100"
                required
              />
            </div>
            {file && (
              <p className="text-xs text-gray-500 flex items-center gap-1 mt-1">
                <FileText className="h-3 w-3" />
                {file.name} ({Math.round(file.size / 1024)} KB)
              </p>
            )}
          </div>
        </CardContent>
        
        <CardFooter>
          <Button 
            type="submit" 
            className="w-full" 
            disabled={isUploading || !file || !title.trim()}
          >
            <Upload className="h-4 w-4 mr-2" />
            {isUploading ? 'Uploading...' : 'Upload Document'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
};

export default DocumentUpload;
