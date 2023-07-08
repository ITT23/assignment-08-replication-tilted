package com.example.tilted;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Build;
import android.widget.Toast;

import androidx.annotation.RequiresApi;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.Base64;
import fi.iki.elonen.NanoHTTPD;


public class Sender extends NanoHTTPD {

    private Context context;
    private File currentFile;

    public Sender(Context context) {
        super(8080);
        this.context = context;
        startWebServer();
    }

    public void setCurrentFile(File currentFile) {
        this.currentFile = currentFile;
    }

    private boolean startWebServer() {
        try {
            start();
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(context, "Webserver could not be started.", Toast.LENGTH_SHORT).show();
        }
        return false;
    }

    private boolean isImage(File file) {
        if (file.getName().contains(".trashed")) return false;
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        Bitmap bitmap = BitmapFactory.decodeFile(file.getAbsolutePath(), options);
        return options.outWidth != -1 && options.outHeight != -1;
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    private String encodeFile(File file) {
        try {
            byte [] encoded = Files.readAllBytes(file.toPath());
            return Base64.getEncoder().encodeToString(encoded);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public Response serve(IHTTPSession session) {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            // only allow throwing if current file is image (not directory)
            /** if (currentFile.isDirectory()) {
                File[] listFiles = currentFile.listFiles();
                String[] bufferedFiles = new String[listFiles.length];
                for (int i = 0; i < listFiles.length; i++) {
                    if (isImage(listFiles[i])) {
                        String encoded = encodeFile(listFiles[i]);
                        if (encoded != null) {
                            bufferedFiles[i] = encoded;
                        }
                    }
                }
                return new Response(Arrays.toString(bufferedFiles));
            } else **/ if (currentFile.isFile() && isImage(currentFile)) {
                return new Response(encodeFile(currentFile));
            }
        }
        return new Response("");
    }
}
