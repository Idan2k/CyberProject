import fcntl
import os
import subprocess

from Target import Target
from Tool import Tool
from Utils import print_blue, print_ok, print_warning, print_fail, bcolors


class SMBClient(Tool):
    class Share:
        def __init__(self, sharename, type, comment):
            self.sharename = sharename
            self.type = type
            self.comment = comment
            self.access = False

    class Server:
        def __init__(self, server, comment):
            self.server = server
            self.comment = comment

    def __init__(self, *args, **kwargs):
        Tool.__init__(self, "SMBClient", *args, **kwargs)

    def nonBlockReadline(self, output):
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.readline()
        except:
            return ''

    def connect_to_share(self, target, share):
        print_blue("Trying to access " + bcolors.HEADER + share.sharename)
        command = ["smbclient", "-N", "//" + str(target.ip) + "/" + share.sharename]
        # print(command)
        done_flag = 0
        try:
            # smbclient = subprocess.check_output(command)
            smbclient2 = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out = smbclient2.stdout
            smbin = smbclient2.stdin
        except subprocess.CalledProcessError:
            print_fail("Share seem inaccessible.")
            return
        while done_flag == 0:
            lines, _ = smbclient2.communicate()
            if b"tree connect failed: NT_STATUS_ACCESS_DENIED" in lines:
                print_fail("Share seem inaccessible.")
                out.close()
                smbin.close()
                return
            elif b"Try \"help\" to get a list of possible commands." in lines:
                print_ok("Share is accessible. run \"smbclient -N //" + str(target.ip) + "/" + share.sharename +"\" manualy.")
                share.access = True
                out.close()
                smbin.close()
                return
            temp = input()
            # line = self.nonBlockReadline(out).decode("utf-8").strip("\n")
            # out.flush()
            # print(line)
            # if line == "" and i == 10:
            #     temp2 = input()
            # elif "tree connect failed: NT_STATUS_ACCESS_DENIED" in line:
            #     print(1)
            #     print_fail("Share seem inaccessible.")
            #     out.close()
            #     smbin.close()
            #     return
            # elif "smb:" in line:
            #     print(3)
            #     print(line)
            #     user_input = input()
            #     print(user_input)
            #     smbclient2.stdin.write(user_input + "\n")
            #     smbin.flush()
            #     if user_input == 'exit' or user_input == 'quit':
            #         smbin.close()
            #         out.close()
            #         done_flag = 1
            # else:
            #     print(2)
            #     print(line)


    def run_and_parse_results(self, target : Target):
        sharename_flag = server_flag = False
        shares = []
        servers = []
        print_blue("Launching smbclient")
        smbclient = subprocess.check_output(["smbclient", "-N", "-L", target.ip, "-g"])
        print_blue("smbclient finished. Processing results.")
        report = ''
        for line in smbclient.decode("utf-8").split("\n"):
            if "Reconnecting" in line:
                print_warning("Ignoring SMB Server information. focusing on shared folders.")
                break
            else:
                share_data = line.split("|")
                new_share = SMBClient.Share(share_data[1], share_data[0], share_data[2])
                shares.append(new_share)
            # if '\t' in line:
            #     if 'Sharename' in line:
            #         sharename_flag = True
            #         print_warning(line)
            #         continue
            #     elif 'Server' in line:
            #         server_flag = True
            #         print("")
            #         print_warning(line)
            #         continue
            #     elif sharename_flag and not server_flag and '----' not in line:
            #         # If we'r here we read a sharename.
            #         data = line.split("      ")
            #         shares.append(SMBClient.Share(data[0].strip(), data[1].strip(), data[2].strip()))
            #     elif sharename_flag and server_flag and '----' not in line:
            #         # If we'r here we read server line.
            #         data = line.split("         ")
            #         servers.append(SMBClient.Server(data[0].strip(), data[1].strip()))
            #     print_ok(line)
            #     report += line + ","
            #     print("")
        print_blue("Found " + str(len(shares)) + " shared folders.\n")
        print_ok("\t" + bcolors.UNDERLINE + "Sharename\tShare Type\t\tComment")
        for share in shares:
            print_ok("\t" + bcolors.HEADER + share.sharename + bcolors.OKGREEN + "\t\t" + share.type + "\t\t" + share.comment)
        for share in shares:
            self.connect_to_share(target, share)
            report += share.sharename + "," + share.type + "," + share.comment + "," + str(share.access) + "|"
        for server in servers:
            print(server.server + ", " + server.comment)
        report = report[:-1]
        target.scans[-1].reports["SMBCLIENT"] = report
