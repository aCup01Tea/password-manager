try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")
 

def search_gg(name_app: str):
    query = f"{name_app} and login"
    
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        print(j)
        return j


# search_gg("VK")
# search_gg("Twich")
# search_gg("Figma")
# search_gg("GitHub")

# search_gg("Gmail") - не находит...
