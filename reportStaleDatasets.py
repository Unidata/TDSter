import os
import json
import io
from helpers.fileName_helper import getOutFileDataPath


aliases = {"NDFD" : ["National Digital Forecast Database"],
           "WWIII" : ["Wave Watch III", "WW3"],
           "RTMA" : ["Real Time Mesoscale Analysis"],
           "RAP" : ["Rapid Refresh"]}

maxAges = {"ncep" :
              {"DGEX" : 16,
               "GEFS": 13,
               "GFS": 11,
               "NAM": {"general" : 9,
                       "NAM CONUS 80km" : 15,
                       "Alaska 22" : 15,
                       "Alaska 45" : 15,
                       "Alaska 95" : 15},
               "RAP" : 3,
               "RTMA" : 4,
               "SREF" : 11,
               "WWIII" : 11,
               "NDFD" : {"CONUS 5km" : 16,
                         "CONUS 5km conduit" : 2,
                         "FireWx" : 6,
                         "general" : 24}
              },
          "fnmoc" :
              {"COAMPS" : 18,
               "FAROP" : 9,
               "NAVGEM" : 12,
               "NCODA" : 23,
               "WWIII" : 18}
         }


def email_report(server, report):
    # Import smtplib for the actual sending function
    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText
    me = "sarms@unidata.ucar.edu"
    rec = "sarms@unidata.ucar.edu"
    report2 = '\n'.join(report)
    msg = MIMEText(report2)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = '[TDSter] Report for {}'.format(server)
    msg['From'] = me
    msg['To'] = rec

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.unidata.ucar.edu')
    s.sendmail(me, [rec], msg.as_string())
    s.quit()



def specialCheckDS(specialCheck, collection, currentAges):
    global report
    global reportType
    collectionChecked = False
    for namType in maxAges[reportType][specialCheck]:
        if namType.lower() in collection.lower():
            if not "CONDUIT" in collection:
                collectionChecked = True
                maxAge = maxAges[reportType][specialCheck][namType]
                currentAge = currentAges[collection]
                if (currentAge > maxAge):
                    report.append("{} is greater than {} hours old (should be less than {} hours old)".format(collection, currentAge, maxAge))

    if not collectionChecked:
        maxAge = maxAges[reportType][specialCheck]["general"]
        currentAge = currentAges[collection]
        if (currentAge > maxAge):
            report.append("{} is greater than {} hours old (should be less than {} hours old)".format(collection, currentAge, maxAge))


def main(testServer):
    global report
    report = []
    global reportType
    reportFileLoc = outFileDataPath = getOutFileDataPath(testServer)
    specialChecks = ["NAM", "NDFD"]
    reportTypes = ["ncep", "fnmoc"]
    for reportType in reportTypes:
        fullReportFileName = "{}_fullReport.json".format(reportType)
        fullReportFile = os.path.join(outFileDataPath, fullReportFileName)
        with io.open(fullReportFile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        currentAges = data["simpleAgeReport"]
        for collection in currentAges:
            collectionChecked = False
            for specialCheck in specialChecks:
                if specialCheck.lower() in collection.lower() and not collectionChecked:
                    collectionChecked = True
                    specialCheckDS(specialCheck, collection, currentAges)
            if not collectionChecked:
                for collectionName in maxAges[reportType]:
                    reportThisCollection = False
                    if collectionName in collection:
                        reportThisCollection = True
                    elif aliases.has_key(collectionName):
                        for alias in aliases[collectionName]:
                            if alias in collection:
                                reportThisCollection = True
                    if reportThisCollection and not collectionChecked:
                        collectionChecked = True
                        maxAge = maxAges[reportType][collectionName]
                        currentAge = currentAges[collection]
                        if (currentAge > maxAge):
                            report.append("{} is greater than {} hours old (should be less than {} hours old)".format(collection, currentAge, maxAge))

    if report != []:
        email_report(testServer, report)

if __name__ == "__main__":
    main("http://thredds.ucar.edu/")