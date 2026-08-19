import re

def split_into_sentences(text:str):
    return re.split(r'(?<=[.!?])\s+',text.strip())

def chunk_text(
        text:str,
        chunk_size:int=1000,
        overlap:int=200
):
    sentences=split_into_sentences(text)
    chunks=[]
    current_chunk=[]
    current_length=0
    chunk_index=0

    for sentence in sentences:
        sentence_length=len(sentence)

        if current_length+sentence_length<=chunk_size:
            current_chunk.append(sentence)
            current_length+=sentence_length+1
        else:
            if current_chunk:
                content=" ".join(current_chunk).strip()
                chunks.append({
                    "chunk_index":chunk_index,
                    "content":content
                })
                chunk_index+=1

            overlap_text=" "
            overlap_length=0

            for previous_sentence in reversed(current_chunk):
                if overlap_length +len(previous_sentence) >overlap:
                    break

                overlap_text=previous_sentence+" "+overlap_text
                overlap_length+=len(previous_sentence)+1
            current_chunk=[]

            if overlap_text.strip():
                current_chunk.append(overlap_text.strip())
                current_length=len(overlap_text.strip())

            else:
                current_length=0

            current_chunk.append(sentence)
            current_length+=sentence_length+1
    if current_chunk:
        content=" ".join(current_chunk).strip()

        chunks.append({
            "chunk_index":chunk_index,
            "content":content
        })

    return chunks


def chunk_pages(pages):
    all_chunks=[]
    for page in pages:
        page_chunks=chunk_text(page["text"])

        for chunk in page_chunks:
            all_chunks.append({
                "page_number":page["page_number"],
                "chunk_index":chunk["chunk_index"],
                "content":chunk["content"]
            })
    return all_chunks