const http: string = "http://";
const domen: string = "localhost";
const port: string = ":8000";
const baseURL: string = http + domen + port;

export const filesPath: string = baseURL + "/files";
export const alertsPath: string = baseURL + "/alerts";

export const filetDownloadPath = (fileID: string): string => {
    return `${filesPath}/${fileID}/download`;
};