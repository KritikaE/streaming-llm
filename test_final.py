import requests
import json
import re

print("Testing streaming endpoint...")
print("=" * 60)

try:
    response = requests.post(
        'https://streaming-llm-7gbl.onrender.com/stream',
        stream=True,
        timeout=60
    )
    
    print(f"Status Code: {response.status_code}")
    print("=" * 60)
    
    if response.status_code == 200:
        print("✅ SUCCESS! Streaming data:\n")
        
        chunk_count = 0
        content = ""
        raw_data = ""
        
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                raw_data += decoded + "\n"
                
                # Show first few chunks
                if chunk_count < 10:
                    print(decoded)
                
                # Parse JSON from each line
                if decoded.startswith('data: '):
                    chunk_count += 1
                    json_part = decoded[6:].strip()  # Remove "data: " prefix
                    
                    if json_part and json_part != '[DONE]':
                        try:
                            parsed = json.loads(json_part)
                            if 'content' in parsed:
                                content += parsed['content']
                        except json.JSONDecodeError as e:
                            print(f"JSON error: {e} | Line: {json_part[:50]}")
        
        print("\n" + "=" * 60)
        print(f"✅ Total chunks received: {chunk_count}")
        print(f"✅ Total characters: {len(content)}")
        print("=" * 60)
        
        # Show a preview of the content
        if content:
            print("\n📄 Content Preview (first 200 chars):")
            print(content[:200])
            print("..." if len(content) > 200 else "")
        
        if chunk_count >= 5 and len(content) >= 800:
            print("\n🎉 ALL REQUIREMENTS MET!")
            print("✅ Streaming: YES")
            print("✅ Multiple chunks: YES (" + str(chunk_count) + " chunks)")
            print("✅ 800+ characters: YES (" + str(len(content)) + " chars)")
            print("✅ Valid JSON format: YES")
            print("\n✅ YOUR URL IS READY TO SUBMIT:")
            print("https://streaming-llm-7gbl.onrender.com/stream")
        else:
            print("\n⚠️ Some requirements not met")
            print(f"Chunks: {chunk_count} (need 5+)")
            print(f"Characters: {len(content)} (need 800+)")
            
            if len(content) == 0:
                print("\n🔍 Debugging: No content extracted. Showing raw data sample:")
                print(raw_data[:500])
            
    else:
        print(f"❌ Error: Status code {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()