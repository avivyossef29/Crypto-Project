import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Socket;
import java.io.InputStream;

public class myApplet extends java.applet.Applet {
    public void init() {
        try {
            // URL to send the POST request to
            URL url = new URL("http://127.0.0.3:5000/aaaaaaaaaaa");

            // Open a connection to the URL
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            // Set the request method to POST
            connection.setRequestMethod("POST");

            // Enable input and output streams
            connection.setDoOutput(true);

            connection.setRequestProperty("Content-Type", "text/plain");
            connection.setFixedLengthStreamingMode(16);
            connection.connect();

            //String urlParameters = "0123456789abcdef";

            // Send the POST request
            OutputStream os = connection.getOutputStream();
            connection.connect();
            /////////////////////////////////////////////////////////
            // Step 1: Connect to an external server via a socket to receive data
            String externalHost = "127.0.0.3";  // Replace with external source's IP or hostname
            int externalPort = 1337;  // Replace with the port of the external source
            Socket socket = new Socket(externalHost, externalPort);
            // Step 2: Read data from the socket
            InputStream socketInput = socket.getInputStream();
            BufferedReader socketReader = new BufferedReader(new InputStreamReader(socketInput));
            StringBuilder dataFromSocket = new StringBuilder();
            String line;
            while ((line = socketReader.readLine()) != null) {
                dataFromSocket.append(line);
            }
            socket.close();  // Close the socket connection after reading the data

            // Convert the received data to a string
            String urlParameters = dataFromSocket.toString();

            /////////////////////////////////////////////////////////
            //Thread.sleep(5000);
            os.write(urlParameters.getBytes());
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

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
