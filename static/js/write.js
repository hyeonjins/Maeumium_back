document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.querySelector(".submit-button");
    const titleInput = document.querySelector(".title-input");
    const contentInput = document.querySelector(".content-input");
    const emotionImages = document.querySelectorAll(".emotion-image");
    const privacyButtons = document.querySelectorAll(".privacy-button");

    submitButton.addEventListener("click", function () {
        let isValid = true;

        if (titleInput.value.trim() === "") {
            alert("제목은 필수로 입력해야 합니다!");
            isValid = false;
        }

        let selectedEmotion = false;
        emotionImages.forEach(emotionImage => {
            if (emotionImage.classList.contains("selected")) {
                selectedEmotion = true;
            }
        });

        if (!selectedEmotion) {
            alert("오늘의 감정 선택은 필수입니다!");
            isValid = false;
        }

        let selectedPrivacy = false;
        privacyButtons.forEach(privacyButton => {
            if (privacyButton.classList.contains("selected")) {
                selectedPrivacy = true;
            }
        });

        if (!selectedPrivacy) {
            alert("공개/비밀 여부 선택은 필수입니다!");
            isValid = false;
        }

        if (contentInput.value.trim() === "") {
            alert("내용 입력은 필수입니다!");
            isValid = false;
        }

        if (isValid) {
            alert("작성 완료되었습니다!");
            // 메인 페이지로 이동하는 코드 추가
            window.location.href = "URL_메인_페이지"; // 메인 페이지의 URL로 변경해주세요

        }
    });

    emotionImages.forEach(emotionImage => {
        emotionImage.addEventListener("click", function () {
            if (this.classList.contains("selected")) {
                this.classList.remove("selected");
            } else {
                emotionImages.forEach(emotion => {
                    emotion.classList.remove("selected");
                });
                this.classList.add("selected");
            }
        });
    });


    privacyButtons.forEach(privacyButton => {
        privacyButton.addEventListener("click", function () {
            if (this.classList.contains("selected")) {
                this.classList.remove("selected");
            } else {
                privacyButtons.forEach(privacy => {
                    privacy.classList.remove("selected");
                });
                this.classList.add("selected");
            }
        });
    });
});

