document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            // console.log(this.currentStep);
            // if (this.currentStep == 3) {
            //     $.ajax({
            //     url: "http://127.0.0.1:8004/addDonation2/", //gdzie się łączymy
            //     type: "post", //typ połączenia, domyślnie get
            //     dataType: "json", //typ danych jakich oczekujemy w odpowiedzi
            //     // contentType: 'json',
            //
            //     data: { //dane do wysyłki
            //
            //
            //     },})
            // }
            console.log(this.currentStep);
            if (this.currentStep == 5)
            {
                                var radios2 = document.getElementsByName('organization');
                for (var i = 0, length = radios2.length; i < length; i++)
                {
                  if (radios2[i].checked)
                  {

                    var organization_id2 = radios2[i].dataset.name;
                    break;
                  }
                }
                // document.querySelector('#summary_quantity').value = document.querySelector('#bags').value;
                document.querySelector('#summary_quantity').innerHTML = document.querySelector('#bags').value;
                document.querySelector('#summary_organization').innerHTML = organization_id2;
                document.querySelector('#summary_address').innerHTML = document.querySelector('#address').value;
                document.querySelector('#summary_city').innerHTML = document.querySelector('#city').value;
                document.querySelector('#summary_postcode').innerHTML = document.querySelector('#postcode').value;
                document.querySelector('#summary_phone').innerHTML = document.querySelector('#phone').value;
                document.querySelector('#summary_data').innerHTML = document.querySelector('#data').value;
                document.querySelector('#summary_time').innerHTML = document.querySelector('#time').value;
                document.querySelector('#summary_text').innerHTML = document.querySelector('#more_info').value;
            }

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();

            this.currentStep++;
            this.updateForm();
            // var csrftoken = $.cookie('csrftoken');

            // function csrfSafeMethod(method) {
            //     // these HTTP methods do not require CSRF protection
            //     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            // }

            // $.ajaxSetup({
            //     beforeSend: function (xhr, settings) {
            //         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            //             xhr.setRequestHeader("X-CSRFToken", csrftoken);
            //         }
            //     }
            // });
            var checkboxes = document.getElementsByName('categories');
            var vals = "";
            for (var i=0, n=checkboxes.length;i<n;i++)
            {
                if (checkboxes[i].checked)
                {
                    vals += " "+checkboxes[i].value;
                }
            }
            if (vals) vals = vals.substring(1);

            var radios = document.getElementsByName('organization');

            for (var i = 0, length = radios.length; i < length; i++)
            {
              if (radios[i].checked)
              {

                var organization_id = radios[i].value;
                break;
              }
            }
            $.ajax({
                url: "http://127.0.0.1:8004/addDonation/", //gdzie się łączymy
                type: "post", //typ połączenia, domyślnie get
                dataType: "json", //typ danych jakich oczekujemy w odpowiedzi
                // contentType: 'json',

                data: { //dane do wysyłki
                    // 'quantity': document.querySelector('bags').value,

                    'quantity':document.querySelector('#bags').value,
                    'categories': 1,

                    'categories2': vals,
                    'institution': organization_id,
                    'address': document.querySelector('#address').value,
                    'phone_number': document.querySelector('#phone').value,
                    'city': document.querySelector('#city').value,
                    'zip_code': document.querySelector('#postcode').value,
                    'pick_up_date': document.querySelector('#data').value,
                    'pick_up_time': document.querySelector('#time').value,
                    'pick_up_comment': document.querySelector('#more_info').value,
                    'user': 3,
                    'csrfmiddlewaretoken': "{{csrf_token}}",


                },
                success: function (data) {
                    console.log(data);
                }

            });
            location.href="/confirmation"
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
