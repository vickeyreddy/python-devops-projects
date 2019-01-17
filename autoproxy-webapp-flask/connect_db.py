import cx_Oracle

class ConnectDB(object):

    def __init__(self, host, port, user, passwd, db):

        self.db_host = host
        self.db_port = port
        self.db_user = user
        self.db_pass = passwd
        self.db_name = db

    def save_subnet(self, group_id, subnet):

        try:
            con = cx_Oracle.connect(self.db_user +'/'+ self.db_pass + '@' + self.db_host + ':' + str(self.db_port) + '/' + self.db_name)
            cur = con.cursor()
            out_parameter = cur.var(cx_Oracle.STRING)
            plsql = "BEGIN atp_web_mgmt.save_net_address(:ip, :gid, :o_message); end;"
            execute_proc = cur.execute(plsql, (subnet, group_id, out_parameter))
            data = out_parameter.getvalue()

        except cx_Oracle.DatabaseError, e:
            error, = e
            data =("Error: %s" % (error.message))
            print data

        else:
            return data;

        finally:
            cur.close()
            con.close()

    def delete_subnet(self, subnet):

        try:
            con = cx_Oracle.connect(self.db_user +'/'+ self.db_pass + '@' + self.db_host + ':' + str(self.db_port) + '/' + self.db_name)
            cur = con.cursor()
            out_parameter = cur.var(cx_Oracle.STRING)
            plsql = "BEGIN atp_web_mgmt.delete_net_address(:in_ip_string, :o_message); end;"
            execute_proc = cur.execute(plsql, (subnet, out_parameter))
            data = out_parameter.getvalue()

        except cx_Oracle.DatabaseError, e:
            error, = e
            data =("Error: %s" % (error.message))
            print data

        else:
            return data;

        finally:
            cur.close()
            con.close()

'''
if __name__ == '__main__':
    d = ConnectDB('p339-0-1-scan.corporate.ge.com', 1621, 'ATPRXADM01', 'ATPRXADM01', 'cig1')
    result_save = d.save_subnet('g99999999', '999.999.999.999_99')
    #result_delete = d.delete_subnet('999.999.999.999_99')
    print result_save
'''
