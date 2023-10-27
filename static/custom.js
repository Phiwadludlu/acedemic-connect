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
                const response = await fetch('/v1/api/get_all_modules', {
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
    created() {
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
        clearSearchText() {
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
            timeslots: [],
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
                const response = await fetch('/v1/api/get_timeslots_by_module', {
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
            if (this.timeslots.length === 0) {
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

app.component('schedule-component', {
    template: `
        <div class="d-flex flex-column gap-2">
            <div class="row">
                <label class="form-label ps-0" for="dayOfWeek">Day</label>
                <select class="form-select" id="dayOfWeek" v-model="selectedDay" aria-label="Default select example">
                    <option selected>Choose a day</option>
                    <option value="Monday">Monday</option>
                    <option value="Tuesday">Tuesday</option>
                    <option value="Wednesday">Wednesday</option>
                    <option value="Thursday">Thursday</option>
                    <option value="Friday">Friday</option>
                </select>
            </div>
            <table class="table" v-if="filteredDays.length">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Start time</th>
                        <th scope="col">End time</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody v-for="(day, index) in filteredDays" :key="'day' + index">
                    <tr v-for="(timeslot, i) in day.timeslots" :key="'timeslot' + i">
                        <th scope="row">{{ i + 1 }}</th>
                        <td><input class="form-control" type="time" v-model="timeslot.start_time" /></td>
                        <td><input class="form-control" type="time" v-model="timeslot.end_time" /></td>
                        <td><span class="mt-2 material-symbols-outlined" style="cursor: pointer;" @click="removeRow(i, timeslot.timeslot_id)">remove</span></td>
                    </tr>
                </tbody>
            </table>
            <div class="row d-flex align-items-center justify-content-end">
                <button v-if="selectedDay !== 'Choose a day'" role="button" style="width: 125px;" id="add-row"
                    class="btn d-flex align-items-center justify-content-center bg-light-subtle border border-1"
                    @click.prevent="addRow()">
                    <span class="material-symbols-outlined">add</span>Add row
                </button>
            </div>
        </div>`,
    setup() {
        const sc = Vue.ref(null);
        return {
            sc
        }
    },
    props: {
        staff_number: {
            type: String,
            default: '',
        }
    },
    data() {
        return {
            days: [],
            selectedDay: 'Choose a day',
            removalStaging: [],
        }
    },
    computed: {
        filteredDays() {
            if (!this.selectedDay) return [];
            return this.days.filter(day => day.day === this.selectedDay);
        }
    },
    methods: {
        addRow() {
            console.log(this.selectedDay);
            const index = this.days.findIndex(item => item === this.days.filter(item => item.day === this.selectedDay)[0]);
            console.log(index);
            if (index === -1) {
                this.days.push({
                    day: this.selectedDay,
                    timeslots: [{timeslot_id : "", start_time: '', end_time: '' }]
                });
            } else {
                this.days[index].timeslots.push({timeslot_id : "", start_time: '', end_time: '' });
            }
        },
        removeRow(timeslotIndex, timeslotId) {
            const dayIndex = this.days.findIndex(item => item === this.days.filter(item => item.day === this.selectedDay)[0]);
            this.days[dayIndex].timeslots.splice(timeslotIndex, 1);
            this.removalStaging.push(timeslotId);
        },
        async fetchTimeslots() {
            try {
                // Replace with your actual API endpoint for moduleItems
                const response = await fetch('/v1/api/get_timeslots_by_staff_number', {
                    mode: 'cors',
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        staff_number: this.staff_number
                    })
                });
                const timeslotsData = await response.json();
                this.days = timeslotsData;
            } catch (error) {
                console.error('Error fetching timeslotsData:', error);
            }
        }
    },
    mounted() {
        this.fetchTimeslots()
    }
});


const vm = app.mount('#app');