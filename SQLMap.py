import subprocess
import sys
import time
from urllib.parse import urlparse

import readchar
import validators
import requests
from Tool import Tool
from Utils import bcolors, safe_print, print_ok, print_blue, print_fail, print_cyan, print_warning, print_header
from WebTarget import WebTarget

br = "--------------------------------------"
delimeter = "-_-"
payload_delimeter = "-----"


class SQLMap(Tool):
    def __init__(self, *args, **kwargs):
        Tool.__init__(self, "SQLMap", *args, **kwargs)
        self.flags = dict({})

    def execute_and_parse_sqlmap(self, command):
        url_parameters_dict = dict({})
        vulner_url = ''
        method_type = ''
        vulner_param = ''
        sqli_type = ''
        sqli_payload = ''
        final_string_value = ''
        my_SQLi_payloads = dict({})
        flag = command.pop()
        utl_flag = 0
        to_insert = ""
        dash_flag = 0
        # safe_print(command)
        form_line = 0
        url_line = 0
        # print(command)
        sqlmap = subprocess.Popen(command, stdout=subprocess.PIPE)
        # sqlmap = subprocess.check_output(command)
        output = sqlmap.stdout
        # HERE output = open("sqlmap.out", "r")

        # print(sqlmap.decode("utf-8"))
        # return
        # event.set()
        cookie_flag = 0
        for entry in command:
            if "--cookie" in entry:
                cookie_flag = 1
        # if "--cookie" in command:
        #     cookie_flag = 1
        # else:
        #     cookie_flag = 0
        # if flag == 'Cookie':
        #     print("It's a cookie check!")
        if flag == 'Parameters':
            form_number = 0
            cur_form_num = 1
        elif flag == 'Cookie':
            final_string_value += "COOKIE" + delimeter
        end_flag = 0
        vulner_flag = 2
        while end_flag == 0:
            # print("inside loop")
            # retcode = sqlmap.poll()
            #  for line in nmap.read().split("\n"):
            # HERE line = output.readline().strip("\n")
            line = output.readline().decode("utf-8").strip("\n")
            # print(line)
            # if "Error" in line:
            if flag == 'Parameters':
                url_line = 0
                form_line = 0
                if '] Form' in line:  # Checks if line informs of Form type SQLi
                    form_line = 1
                elif '] URL' in line:  # Checks if line informs of URL type SQLi
                    url_line = 1
                if form_line or url_line:
                    dash_flag = 0   # SQLMap informs of payload with triple dashes (---)
                    if form_number == 0:  # Only for first form
                        form_number = int(line.split(" ")[0].split("/")[1].replace("]", ""))
                        print_blue("Found " + str(form_number) + " possible vulnerable places:\n"
                                   + br + "\n\t\t1/" + str(form_number))
                    # reading 3 lines
                    if form_line == 1:  # Parse the first line of sqlmap's form report
                        form_line = 0
                        url_line = 0
                        print_blue("SQLi Place:\tHTTP Request")
                        http_request_info_line = output.readline().decode("utf-8").strip("\n")
                        # HERE http_request_info_line = output.readline().strip("\n");
                        if cookie_flag:  # If the user provided cookies, next line will involve the cookie
                            cookie_line = output.readline().decode("utf-8").strip("\n").strip(" ")
                            # HERE cookie_line = output.readline().strip("\n").strip(" ")
                            cookie = cookie_line.split(": ")[1].replace(";", ",")
                            cookie = cookie[:-1]
                            cookie += '\"'
                        data_line = output.readline().decode("utf-8").strip("\n")
                        # HERE data_line = output.readline().strip("\n")
                        # print(data_line)
                        # manipulations
                        method_type = http_request_info_line.split(' ')[0]
                        vulner_url = http_request_info_line.split(' ')[1]
                        # final_string_value += method_type + delimeter
                        if method_type == 'POST':
                            data = data_line.split(" ")[2]
                            print_blue("URL:     \t" + vulner_url + "\nMethod Type:\t" + method_type +
                                       "\nPOST Data:\t" + data)
                            if cookie_flag:
                                to_insert = method_type + "," + data + "," + cookie
                                print_blue("Cookie:     \t" + cookie + "\n")
                            else:
                                to_insert = method_type + "," + data
                                safe_print("")
                        else:  # GET Request
                            print_blue("URL:     \t" + vulner_url + "\nMethod Type:\t" + method_type)
                            if cookie_flag:
                                to_insert = method_type + "," + cookie
                                print_blue("Cookie:     \t" + cookie + "\n")
                            else:
                                to_insert = method_type
                                safe_print("")
                        # if vulner_flag == 0:
                        #     safe_print(
                        #         bcolors.FAIL + bcolors.BOLD + "[-] Parameters seem invulnerable to SQLI." + bcolors.OKBLUE + bcolors.BOLD + br
                        #         + "\n\t\t" + str(cur_form_num) + "/" + str(form_number) + bcolors.ENDC)
                        #     cur_form_num += 1
                        # elif vulner_flag == 1:
                        #     vulner_flag = 0
                        # else:
                        #     vulner_flag = 0
                        # http://siteURL, cookie=a, coupon.

                        # print(vulner_url + " " + to_insert)
                        url_parameters_dict[vulner_url] = to_insert
                    elif url_line:
                        URL = output.readline().decode("utf-8").strip("\n").split(" ")[1]
                        # HERE URL = output.readline().strip("\n").split(" ")[1]
                        print_blue("SQLi Place:\tHTTP Request\nURL:     \t" + URL + "\nMethod Type:\tGET\n")
                        if cur_form_num < form_number:
                            url_flag = 1
                # forms[form_number] = vulner_url + ", " + cookie + ", " + data
            # elif flag == "Cookie":

            if '[ERROR] all tested parameters do not appear to be injectable.' in line:
                cur_form_num += 1
                if flag == 'Parameters':
                    print_fail("[-] Parameters seem invulnerable to SQLi.")
                    if cur_form_num <= form_number:
                        print_blue(br + "\n\t\t" + str(cur_form_num) + "/" + str(form_number))
                elif flag == 'Cookie':
                    print_fail("[-] Cookie seem invulnerable to SQLi.")
                    print_blue(br + "\n\t\t" + str(cur_form_num) + "/" + str(form_number))
                url_flag = 0
            elif '---' in line:  # vulnerabilities found
                parameter_info = output.readline().decode("utf-8").strip("\n").split(" ")
                # HERE parameter_info = output.readline().strip("\n").split(" ")
                # Adding parameter name and HTTP method type
                # , coupon, POST
                vulner_param = parameter_info[1]
                final_string_value += method_type + delimeter + vulner_param + delimeter
                if flag == 'Parameters':
                    print_ok("[+] Parameter \"" + parameter_info[1] + "\" was found vulnerable to SQLi!\n")
                elif flag == 'Cookie':
                    print_ok("[+] Cookie \"" + parameter_info[1] + "\" was found vulnerable to SQLi!\n")
                to_insert += ", " + parameter_info[1] + ", " + parameter_info[2].replace("(", "").replace(")", "")
                vulner_flag = 1
                while dash_flag == 0:
                    dash_line = output.readline().decode("utf-8").strip("\n")
                    # HERE dash_line = output.readline().strip("\n")
                    if '---' in dash_line:  # End of vulnerabilities.
                        my_SQLi_payloads[vulner_url] = final_string_value
                        # print("\n\n\n" + final_string_value + "\n" + my_SQLi_payloads[vulner_url] + "\n\n\n")
                        final_string_value = ''
                        dash_flag = 1
                        if flag == 'Parameters':
                            if cur_form_num < form_number:
                                cur_form_num += 1
                                print_blue(br + "\n\t\t" + str(cur_form_num) + "/" + str(form_number))
                    elif dash_line.strip() != "":  # Parsing a vulner
                        sqli_type = dash_line.split(": ")[1].replace("\n", "")
                        title = output.readline().decode("utf-8").strip("\n").split(": ")[1].replace("\n", "")
                        # HERE title = output.readline().strip("\n").split(": ")[1].replace("\n", "")
                        payload = output.readline().decode("utf-8").strip("\n").split(": ")[1]
                        # HERE payload = output.readline().strip("\n").split(": ")[1]
                        print_ok(bcolors.UNDERLINE + "\tSQLi Type:\t" + bcolors.ENDC + bcolors.OKCYAN + sqli_type + " - " + title)
                        print_ok(bcolors.UNDERLINE + "\tPayload:\t" + bcolors.ENDC + bcolors.OKCYAN + payload + "\n")
                        final_string_value += sqli_type + delimeter + title + delimeter + payload + payload_delimeter
                # print(bcolors.OKGREEN + bcolors.BOLD + "" + bcolors.ENDC)
            elif 'ending @' in line:
                end_flag = 1
                if vulner_flag == 0 or vulner_flag == 2:
                    if flag == 'Parameters':
                        print_fail("[-] Parameters seem invulnerable to SQLi.")
                    elif flag == 'Cookie':
                        print_fail("[-] Cookie seem invulnerable to SQLi.")
                print_blue(br)
                vulner_flag = 0
            elif '(XSS)' in line:
                print_cyan("Potential XSS injection found! if xsser didn't find any payloads,"
                           " you should test it manualy.")
                target_parameter = line.split("\'")[1]
                safe_print(bcolors.OKBLUE + "Testing form for XSS." + bcolors.ENDC)
                # HERE self.brute_xss(vulner_url, to_insert, target_parameter)
            elif 'timed out' in line:
                print_fail("Connection timed out. either the server is offline or you'r not connected to the internet.")
            # event.set()
        # print(bcolors.OKBLUE + bcolors.BOLD + "sqlmap finished. Processing results." + bcolors.ENDC)
        if flag == 'Parameters':
            print_blue("\n")
        # for key in my_SQLi_payloads:
        #     print(key)
        #     print(my_SQLi_payloads[key])
        #     print("---")
        return my_SQLi_payloads

    def check_sql_injection(self, web_target: WebTarget, scan, port):
        # safe_print(bcolors.HEADER + bcolors.BOLD + "Crawling website and checking forms for SQLi." + bcolors.ENDC)
        self.check_sql_injection_forms(web_target, scan, port)
        # self.flags["--cookie"] = "name=nitz;PHPSESSID=88obovgb6rsloa4tag2oeiua7d" # Delete this.
        print_header(bcolors.BOLD + "----Checking Cookies for SQLi----")
        print_blue("\n")
        # self.check_sql_injection_cookies(web_target, scan)

    def check_sql_injection_forms(self, web_target: WebTarget, scan, port):
        print_blue("Checking website for SQL injection.")
        command = ["sqlmap", "-u"]
        # Adding target to the command
        if web_target.homepage != "":
            command.append(web_target.homepage)
        else:
            command.append(web_target.ip + ":" + port)
        # Adding cookies
        # if "--cookie" in self.flags:
        cookie_flag = 1
        cookie_string = ""
        # print(web_target.user_cookies)
        i = 0
        # for cookie in web_target.user_cookies:
        #     cookie_string += cookie + '=' + web_target.user_cookies[i] + ';'
        #     i += 1
        # cookie_string = cookie_string[:-1]
        # cookie_string += "\""
        if web_target.user_cookies:
            for cookie in web_target.user_cookies:
                cookie_string += cookie + "=" + web_target.user_cookies[cookie] + ";"
            cookie_string = cookie_string[:-1]
            command.append("--cookie=" + "\"" + cookie_string + "\"")
            # print(command)
            self.flags["--cookie"] = web_target.user_cookies
        # Adding web crawler with logout exclution, forms sql injection checks and batch execution.:
        command += ["--crawl", "5", "--crawl-exclude=logout", "--forms", "--batch",
                    '--answers="keep testing=Y,skip further tests=n"', "Parameters"]
        # print(command)
        scan.reports["SQLiReport"] = self.execute_and_parse_sqlmap(command)

    def get_cookies(target):
        global site_cookies
        session = requests.Session()
        response = session.get(target)
        # print(session.cookies.get_dict())
        site_cookies = session.cookies.get_dict()

    def check_sql_injection_cookies(self, target, scan):
        # if not self.user_cookies:
        #     # get_cookies(target)
        #     self.parse_cookies(self.flags["--cookie"])
        # Crafting base command
        command = ["sqlmap", "-u", target.ip, "--level", "2", '--batch', "--answers='keep testing=Y,skip further tests=n'"]
        cookies = self.flags["--cookie"].split(";")
        for cookie in cookies:
            end_flag = 0
            # --cookie="cookie=1" -p "cookie"
            print_blue("Testing cookie \"" + cookie + "\" for vulnerabilities.\n")
            command.append("--cookie=" + self.flags["--cookie"])
            command.append('-p')
            command.append(cookie.split("=")[0])
            # safe_print("Execute command:")
            command.append("Cookie")
            # safe_print(command)
            self.execute_and_parse_sqlmap(command)
            command.pop()
            command.pop()
            command.pop()
        print_header("Cookie check done.")

    def brute_xss(self, vulner_url, params, target_parameter):
        # method_type / method_type,cookie / method_type,data / method_type,data,cookie
        split_params = params.split(",")
        command = ["xsser", '-u']
        if split_params[0] == 'POST':
            command.append(vulner_url)
            command.append("-p")
            # print(split_params[1])
            params2 = split_params[1].split("&")
            new_data = ''
            for param in params2:
                split = param.split('=')
                temp2 = split[0]
                if split[0] == target_parameter:
                    temp2 += '=XSS'
                else:
                    temp2 += '=' + split[1]
                new_data += temp2 + '&'
            last_data = new_data[:-1]
            command.append(last_data)  # adding POST data
            # method_type, data OR method_type, cookie, data
        elif split_params[0] == 'GET' or split_params[0] == 'G':
            protocol = vulner_url.split("://")[0]
            temp = urlparse(vulner_url)
            domain = temp.netloc
            path = temp.path
            query = temp.query
            params2 = query.split("&")
            new_query = ''
            for param in params2:
                split = param.split('=')
                temp2 = split[0]
                if split[1] == '' or len(params2) == 1:
                    temp2 += '=XSS'
                else:
                    temp2 += '=' + split[1]
                new_query += temp2 + '&'
            last_query = new_query[:-1]
            target_url = protocol + "://" + domain
            path_with_query = path + "?" + last_query
            command.append(target_url)
            command.append("-g")
            command.append(path_with_query)

        # Cookies
        if "--cookie" in self.flags:
            # cookie_string = "\""
            # if not self.user_cookies:
            #     self.parse_cookies(self.flags['--cookie'])
            # for cookie in self.user_cookies:
            #     cookie_string += cookie + '=' + self.user_cookies[cookie] + '; '
            # cookie_string += "\""
            command.append("--cookie=" + "\"" + self.flags["--cookie"] + "\"")
        # method_type OR method_type + cookie
        command.append("--payload=\'alert(XSS)\'")
        # command.append("--Fp=\'<script>alert(\"XSS\")</script>\'")
        # HERE print(command)
        xsser = subprocess.check_output(command)
        payload_flag = 0
        for line in xsser.decode("utf-8").split("\n"):
            if 'Final Attack' in line:
                payload_flag = 1
                payload = line.split(" ")[3]
                safe_print(bcolors.OKGREEN + bcolors.BOLD + "    [+] XSS Payload: " + payload + bcolors.ENDC)
        if payload_flag == 0:
            safe_print(bcolors.FAIL + "xsser finished and found no payloads.\n" + bcolors.ENDC)