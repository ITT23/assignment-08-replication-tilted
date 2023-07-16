package com.example.tilted;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Build;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.RequiresApi;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Base64;
import fi.iki.elonen.NanoHTTPD;


public class Sender extends NanoHTTPD {

    private MainActivity context;
    private File currentFile;

    public Sender(Context context) {
        super(8080);
        this.context = (MainActivity) context;
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
        if (context.isImageViewerFragment()) {
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                // only allow throwing if current file is image (not directory)
                if (currentFile.exists() && isImage(currentFile)) {
                    String filename = currentFile.getName();
                    String filedata = encodeFile(currentFile);
                    String msg = String.format("{\"filename\" : \"%s\", \"data\" : \"%s\"}", filename, filedata);
                    return new Response(msg);
                }
            }
        }
        return new Response(Response.Status.NOT_FOUND, MIME_PLAINTEXT, "The requested resource is not an image.");
    }
}
