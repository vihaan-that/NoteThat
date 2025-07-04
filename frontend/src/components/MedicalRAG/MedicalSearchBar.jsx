import React, { useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search } from "lucide-react";

/**
 * MedicalSearchBar component for querying the medical RAG system
 */
const MedicalSearchBar = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex w-full gap-2">
      <Input
        type="text"
        placeholder="Ask a medical question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1"
        disabled={isLoading}
      />
      <Button 
        type="submit" 
        disabled={!query.trim() || isLoading}
        className="bg-blue-600 hover:bg-blue-700"
      >
        <Search className="h-4 w-4 mr-2" />
        {isLoading ? 'Searching...' : 'Search'}
      </Button>
    </form>
  );
};

export default MedicalSearchBar;
