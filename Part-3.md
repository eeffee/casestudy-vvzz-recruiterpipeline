Part 3 - Future AI/RAG Extension

Focus: assist the recruiter searches for talent that match a job. recruiter can ask questions, wants summaries, can reach to the candidate.

Data to include in RAG:   

                          - Job descriptions(Part 1)
                         - Talent profile (this can be created with manipulation of talent DB)
                         - company enrichment data 

How to structure and index: 

                         - split job descriptions and talent profiles for small tokens
                         - generate embeddings using pre-trained models such as BERT or any LLM
                         - use pgvector to store
                         - index metadata (ids, jobdesc,candid,company)
                         - so we created vector and metadata 
                         - hybrid search is applicable using vector and keywords

Metadata and access control:

                         - each talent vector connected with recruiter id can be accesible
                         - apply filtering at any time

Update strategy: 

                        - new talents or jobs can be embedded and insert
                        - weekly refresh for updated profiles
Failure modes:

                        - hallucination
                        - irrelavant talents might return
                            
                        

