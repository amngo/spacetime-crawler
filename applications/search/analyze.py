import os
import codecs

class analyze(object):
    '''
    Analyzing the project
    '''
    def __init__(self):
        pass
    
    # ANALYTICS PART 1
    def Total_Subdomains(self):
        filepath = "analytics/subdomains"
        subdomain_list = os.listdir(filepath)

        
        number_files = len(subdomain_list)
        
        content = "ANALYTICS PART 1\nTotal count of subdomains: {number_files}\n".format(number_files=number_files)
        self.writeToFile("analyze.txt", content, 'a+')
        
        
    def URLs_from_Subdomain(self):
        filepath = "analytics/subdomains"
        subdomain_list = os.listdir(filepath)
        for subdomain in subdomain_list:
            finalpath = "{filepath}/{subdomain}".format(filepath= filepath, subdomain=subdomain)
            with codecs.open(finalpath, 'r',encoding="utf-8") as f:
                number_of_URLs = len(f.read().split("\n"))
                
                content = "{subdomain}::{number_of_URLs}\n".format(subdomain=subdomain.split(".")[0], number_of_URLs=number_of_URLs)
                self.writeToFile("analyze.txt", content, 'a+')
                
                
    def writeToFile(self, filename, content, mode):
        directory = "analytics"
        filePath = "{dir}/{filename}".format(dir=directory,filename=filename)
    
        with codecs.open(filePath, mode,encoding="utf-8") as f:
            f.write(content)
            
    # ANALYTICS PART 2
    def count_invalid_links(self):
        filepath = "analytics/invalid_links.txt"
        with codecs.open(filepath, 'r', encoding="utf-8") as f:
            number_of_invalid_links = len(f.read().split("\n"))
            content = "\nANALYTICS PART 2\nNumber of invalid links it received from the frontier: {number_of_invalid_links}\n".format(number_of_invalid_links=number_of_invalid_links)
            self.writeToFile("analyze.txt", content, 'a+')

    # ANALYTICS PART 3
    def most_outlinks(self):
        filepath = "analytics/outlink_max.txt"
        with codecs.open(filepath, 'r', encoding="utf-8") as f:
            outlink = f.read()
            content = "\nANALYTICS PART 3\nPage with the most out links\n{outlink}".format(outlink=outlink)
            self.writeToFile("analyze.txt", content, 'a+')
            
    # ANALYTICS PART 4(additional)

if __name__ == '__main__':
    a = analyze()
    a.Total_Subdomains()
    a.URLs_from_Subdomain()
    a.count_invalid_links()
    a.most_outlinks()