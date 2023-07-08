package com.example.tilted;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Base64;
import fi.iki.elonen.NanoHTTPD;


public class Sender extends NanoHTTPD {

    public Sender() {
        super(8080);
    }

    @Override
    public Response serve(IHTTPSession session) {
        // todo: get file
        File file = new File("/drawable/test.png");
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            try {
                byte[] encoded = Files.readAllBytes(file.toPath());
                String msg = Base64.getEncoder().encodeToString(encoded);
                return new Response(msg);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return null;
    }
}
