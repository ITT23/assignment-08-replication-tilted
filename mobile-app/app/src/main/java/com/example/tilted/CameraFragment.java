package com.example.tilted;
import android.net.Uri;
import android.os.Bundle;

import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.core.content.FileProvider;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import java.io.File;


public class CameraFragment extends Fragment {

    private View view;
    private Button startCameraBtn;
    private ActivityResultLauncher<Uri> cameraLauncher;
    private Uri imgUri;
    private MainActivity mainActivity;


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        view = inflater.inflate(R.layout.fragment_camera, container, false);
        mainActivity = (MainActivity) getActivity();

        imgUri = createUri();
        registerPictureLauncher();

        startCameraBtn =(Button) view.findViewById(R.id.camera_btn);
        startCameraBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                cameraLauncher.launch(imgUri);
            }
        });

        return view;
    }

    private void registerPictureLauncher() {
        cameraLauncher = registerForActivityResult(
            new ActivityResultContracts.TakePicture(),
            new ActivityResultCallback<Boolean>() {
                @Override
                public void onActivityResult(Boolean result) {
                    try {
                        if (result) {
                            File file = new File(mainActivity.getFilesDir(), "camera_photo.jpg");
                            mainActivity.setChosenFile(file);
                            mainActivity.getSender().setCurrentFile(file);
                            FragmentManager fragmentManager = mainActivity.getSupportFragmentManager();
                            FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
                            fragmentTransaction.replace(R.id.fragment_container, new ImageViewerFragment());
                            fragmentTransaction.addToBackStack(null);
                            fragmentTransaction.commit();
                        }
                    } catch (Exception e) {
                        e.getStackTrace();
                    }
                }
            }
        );
    }

    private Uri createUri() {
        File imgFile = new File(getActivity().getApplicationContext().getFilesDir(), "camera_photo.jpg");
        return FileProvider.getUriForFile(
                getActivity().getApplicationContext(),
                "com.example.tilted.fileProvider",
                imgFile
        );
    }
}