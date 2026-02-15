import requests

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
        
        for line in response.iter_lines():
            if line:
                chunk_count += 1
                decoded = line.decode('utf-8')
                
                # Show first few chunks
                if chunk_count <= 10:
                    print(decoded)
                
                # Extract actual content
                if "'content':" in decoded:
                    try:
                        char = decoded.split("'content': '")[1].split("'")[0]
                        char = char.replace('\\n', '\n').replace("\\'", "'")
                        content += char
                    except:
                        pass
        
        print("\n" + "=" * 60)
        print(f"✅ Total chunks received: {chunk_count}")
        print(f"✅ Total characters: {len(content)}")
        print("=" * 60)
        
        if chunk_count >= 5 and len(content) >= 800:
            print("\n🎉 ALL REQUIREMENTS MET!")
            print("✅ Streaming: YES")
            print("✅ Multiple chunks: YES")
            print("✅ 800+ characters: YES")
            print("\n✅ YOUR URL IS READY TO SUBMIT:")
            print("https://streaming-llm-7gbl.onrender.com/stream")
        else:
            print("\n⚠️ Some requirements not met")
            print(f"Chunks: {chunk_count} (need 5+)")
            print(f"Characters: {len(content)} (need 800+)")
    else:
        print(f"❌ Error: Status code {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")