const app = Vue.createApp({
    data() {
        return {
            moduleItems: [],
            selectedModule: '',
            isDropdownOpen: false,
        };
    },
    methods: {
        updateSelectedModule(newVal) {
            this.selectedModule = newVal;
        },
        updateOpenDropdown(newVal) {
            this.isDropdownOpen = newVal;
        },
        async fetchModuleItems() {
            try {
                // Replace with your actual API endpoint for moduleItems
                const response = await fetch('/v1/api/fetch_modules', {
                    mode: 'cors',
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                const moduleItemsData = await response.json();
                this.moduleItems = moduleItemsData;
            } catch (error) {
                console.error('Error fetching moduleItems:', error);
            }
        },
    },
    created () {
        this.fetchModuleItems();
    }
});

app.component('multiselect', {
    template: '#multiselect-template',
    setup() {
        const ms = Vue.ref(null);
        return {
            ms
        }
    },
    props: {
        searchFieldId: String,
        dropdownId: String,
        limit: Number,
        items: Array,
        checkboxType: String,
        isDropdownOpen: {
            type: Boolean,
            default: false,
        }
    },
    data() {
        return {
            searchText: '',
            currentTags: [],
        };
    },
    computed: {
        filteredItems() {
            return this.items.filter(item => {
                const isMatch = item.name.toLowerCase().includes(this.searchText.toLowerCase()) || item.code.toLowerCase().includes(this.searchText.toLowerCase());
                return isMatch;
            });
        },
        isDropdownDisabled() {
            return this.currentTags.length === this.limit;
        },
    },
    methods: {
        fetchSearch(value) {
            this.searchText = value;
            if (this.searchText) {
                this.$emit('open-dropdown', true);
            } else {
                this.$emit('open-dropdown', false);
            }
        },
        clearSearchText(){
            this.searchText = '';
        },
        debounceInput(id) {
            let timeoutId;
            const waitTime = 800;

            const input = document.getElementById(id);
            input.addEventListener('keyup', (e) => {
                const text = e.currentTarget.value;

                clearTimeout(timeoutId);

                timeoutId = setTimeout(() => {
                    this.fetchSearch(text);
                }, waitTime);
            });
        },
        async handleDropdownClick(value) {
            if (this.currentTags.includes(value)) {
                this.currentTags = this.currentTags.filter(tag => tag !== value);
            } else {
                this.currentTags.push(value);
            }
            this.clearSearchText();
            this.$emit('selected-module', this.currentTags[0]);
            this.$emit('open-dropdown', false);
        },
        handleTagClick(tag) {
            // Remove the clicked tag from currentTags
            this.currentTags = this.currentTags.filter(t => t !== tag);
            this.clearSearchText();
        },
    },
    mounted() {
        this.debounceInput('multiselect-searchfield');
    },
});

app.component('sessionpicker', {
    template: '#session-template',
    setup() {
        const sp = Vue.ref(null);
        return {
            sp
        }
    },
    props: {
        module: {
            type: String,
            default: '',
        }
    },
    data() {
        return {
            selectedDay: "",
            selectedTime: "",
            timeslots : [],
        };
    },
    methods: {
        getDayOfWeek(dateString) {
            const date = new Date(dateString);
            const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
            return days[date.getDay()];
        },
        async fetchTimeslots() {
            try {
                // Replace with your actual API endpoint for moduleItems
                const response = await fetch('/v1/api/fetch_timeslots_by_module', {
                    mode: 'cors',
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        module_code: this.module
                    })
                });
                const timeslotsData = await response.json();
                this.timeslots = timeslotsData;
                console.log(timeslotsData);
            } catch (error) {
                console.error('Error fetching timeslotsData:', error);
            }
        },
    },
    watch: {
        selectedDay(newValue, oldValue) {
            console.log(this.selectedDay);
            console.log(this.module);
            if (this.timeslots.length === 0){
                this.fetchTimeslots();
            }
        },
        module(newVal, oldValue) {
            this.timeslots = [];
        }
    },
    computed: {
        timeOptions() {
            if (this.selectedDay) {
                const selectedDayTimeslots = this.timeslots.find(dayData => dayData.day.toLowerCase() === this.getDayOfWeek(this.selectedDay).toLowerCase());

                if (selectedDayTimeslots) {
                    return selectedDayTimeslots.timeslots.map(slot => ({
                        value: slot.timeslot_id,
                        label: `${slot.period.start_time}-${slot.period.end_time}`,
                    }));
                }
            }
            return [];
        },
    },
});

const vm = app.mount('#app');