<template>
    <el-form
        ref="form"
        v-bind="useProp(schema, 'form')"
        v-on="useEvent(schema)"
        @submit.prevent
    >
        <el-row :gutter="schema.gutter">
            <template
                v-for="(formItem, formIndex) in schema.formItems"
                :key="getItemKey(formItem, formIndex)"
            >
                <div
                    v-if="formItem.type === 'title'"
                    class="sc-form-title"
                    v-bind="useProp(formItem)"
                >
                    {{ formItem.content }}
                </div>

                <component
                    :is="formItem.tag"
                    v-else-if="formItem.type === 'component'"
                    v-bind="useProp(formItem)"
                    v-on="useEvent(formItem)"
                >
                    {{ formItem.content }}
                </component>

                <el-col
                    v-else-if="formItem.show !== false"
                    :span="schema.colSpan"
                    :offset="formItem.offset"
                    :class="{ inline: schema.inline }"
                >
                    <el-form-item v-bind="useProp(formItem, 'item')">
                        <template
                            v-for="(item, itemIndex) in getFormControls(formItem)"
                            :key="getItemKey(item, itemIndex)"
                        >
                            <el-button
                                v-if="isType(item, ['button'])"
                                v-bind="useProp(item)"
                                v-on="useEvent(item)"
                                :v-has-permission="item.hasPermission"
                            >
                                {{ item.content }}
                                <el-icon
                                    v-if="item.rightIcon"
                                    class="el-icon--right"
                                    aria-hidden="true"
                                >
                                    <component :is="item.rightIcon" />
                                </el-icon>
                            </el-button>

                            <el-dropdown
                                v-else-if="isType(item, ['dropdown'])"
                                v-bind="useProp(item)"
                                v-on="useEvent(item)"
                                :v-has-permission="item.hasPermission"
                            >
                                <el-button :type="item.subtype">
                                    {{ item.content }}
                                    <el-icon class="el-icon--right" aria-hidden="true">
                                        <ArrowDown />
                                    </el-icon>
                                </el-button>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item
                                            v-for="(menu, menuIndex) in item.menus"
                                            v-show="menu.show !== false"
                                            :key="menu.name || menuIndex"
                                            @click="useFn(menu.click, $event)"
                                        >
                                            {{ menu.name }}
                                        </el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>

                            <el-input
                                v-else-if="isType(item, ['input'])"
                                v-bind="useProp(item)"
                                v-on="useEvent(item)"
                                @keyup="handleKeyup(item, $event)"
                            >
                                <template v-if="item.append" #append>
                                    {{ item.append }}
                                </template>
                            </el-input>

                            <component
                                :is="fixType(item.type)"
                                v-else-if="isElementControl(item)"
                                v-bind="useProp(item)"
                                v-on="useEvent(item)"
                            >
                                <template v-if="isType(item, ['select'])">
                                    <el-option
                                        v-for="option in item.options"
                                        :key="getOptionValue(item, option)"
                                        :label="getOptionLabel(item, option)"
                                        :value="getOptionValue(item, option)"
                                        :disabled="option.disabled"
                                    />
                                </template>

                                <template v-else-if="isType(item, ['radio', 'radio-group'])">
                                    <component
                                        :is="item.button ? 'el-radio-button' : 'el-radio'"
                                        v-for="option in item.options"
                                        v-bind="useProp(option, 'radio-options')"
                                        :key="option.value"
                                        :value="option.value"
                                    >
                                        {{ option.label }}
                                    </component>
                                </template>

                                <template v-else-if="isType(item, ['checkbox', 'checkbox-group'])">
                                    <component
                                        :is="item.button ? 'el-checkbox-button' : 'el-checkbox'"
                                        v-for="option in item.options"
                                        v-bind="useProp(option, 'checkbox-options')"
                                        :key="option.value"
                                        :value="option.value"
                                    >
                                        {{ option.label }}
                                    </component>
                                </template>
                            </component>

                            <el-upload
                                v-else-if="isType(item, ['upload'])"
                                v-bind="useProp(item)"
                                v-on="useEvent(item)"
                            >
                                <el-button v-if="typeof item.children === 'undefined'" type="primary">
                                    请选择
                                </el-button>
                                <template v-if="Array.isArray(item.children)">
                                    <component
                                        :is="child.tag"
                                        v-for="(child, childIndex) in item.children"
                                        v-show="child.show !== false"
                                        v-bind="useProp(child, 'children')"
                                        :key="child.key || childIndex"
                                    >
                                        {{ child.content }}
                                    </component>
                                </template>
                                <slot
                                    v-else-if="typeof item.children === 'string'"
                                    :name="item.children"
                                />
                                <sc-template
                                    v-else-if="typeof item.children === 'function'"
                                    :content="item.children.call(schema.bind)"
                                    :data="{ bind: schema.bind }"
                                />
                            </el-upload>

                            <el-transfer
                                v-else-if="isType(item, ['transfer'])"
                                v-bind="useProp(item)"
                                v-on="useEvent(item)"
                            >
                                <template v-if="Array.isArray(item.children)">
                                    <component
                                        :is="child.tag"
                                        v-for="(child, childIndex) in item.children"
                                        v-show="child.show !== false"
                                        v-bind="useProp(child, 'children')"
                                        :key="child.key || childIndex"
                                    >
                                        {{ child.content }}
                                    </component>
                                </template>
                                <slot
                                    v-else-if="typeof item.children === 'string'"
                                    :name="item.children"
                                />
                                <sc-template
                                    v-else-if="typeof item.children === 'function'"
                                    :content="item.children.call(schema.bind)"
                                    :data="{ bind: schema.bind }"
                                />
                            </el-transfer>

                            <div
                                v-else-if="item.type === 'html'"
                                v-html="item.content"
                            />
                            <span v-else-if="item.type === 'text'">{{ item.content }}</span>
                            <slot v-else-if="item.type === 'slot'" :name="item.name" />
                            <span v-else>无法匹配“{{ item.type }}”控件</span>
                        </template>
                    </el-form-item>
                </el-col>
            </template>
        </el-row>
    </el-form>
</template>

<script setup>
import { ArrowDown } from '@element-plus/icons-vue';
import { cloneDeep, get, set } from 'lodash-es';
import {
    computed,
    getCurrentInstance,
    onMounted,
    reactive,
    ref,
    toRefs,
} from 'vue';

defineOptions({
    name: 'ScForm',
});

const ELEMENT_CONTROL_TYPES = [
    'select',
    'cascader',
    'radio',
    'radio-group',
    'checkbox',
    'checkbox-group',
    'input-number',
    'switch',
    'slider',
    'rate',
    'color-picker',
    'time-picker',
    'date-picker',
];

const props = defineProps({
    schema: {
        type: Object,
        required: true,
    },
    modelValue: {
        type: Object,
        default: null,
    },
    setting: {
        type: Object,
        default: () => ({
            form: {
                labelSuffix: ':',
                size: 'default',
                class: 'outer_form',
            },
            item: {},
            button: {},
            input: {
                autocomplete: 'off',
            },
            select: {},
            cascader: {},
            radio: {},
            checkbox: {},
            upload: {},
        }),
    },
});
const emit = defineEmits(['update:modelValue']);
const { schema, modelValue, setting } = toRefs(props);
const form = ref(null);
const internalModel = reactive({});
const defaultValue = Object.freeze(cloneDeep(modelValue.value || schema.value.model || {}));
const instance = getCurrentInstance();
const formInstance = computed(() => form.value);

function getFormModel() {
    return schema.value.model || modelValue.value || internalModel;
}

function getFormControls(formItem) {
    if (!formItem.items) {
        return [formItem];
    }
    return Array.isArray(formItem.items) ? formItem.items : [formItem.items];
}

function getItemKey(item, index) {
    return item.key || item.field || item.name || (item.type || 'item') + '-' + index;
}

function getOptionLabel(item, option) {
    return option[item.props?.label || 'label'];
}

function getOptionValue(item, option) {
    return option[item.props?.value || 'value'];
}

function getType(type = '') {
    return type.split('.')[0];
}

function getModifier(type = '') {
    return type.split('.')[1];
}

function useProp(prop = {}, requestedType) {
    const {
        type: rawType = '',
        model,
        field,
        label,
        items,
    } = prop;
    const type = requestedType || getType(rawType);
    const systemTypes = [
        'form',
        'item',
        'radio-options',
        'checkbox-options',
        'children',
        'title',
        'component',
    ];
    const invalidProps = [
        'type',
        'tag',
        'content',
        'children',
        'show',
        'items',
        'on',
        'model',
        'field',
        'offset',
        'hasPermission',
        'rightIcon',
    ];
    const componentProps = {};

    Object.entries(prop).forEach(([key, value]) => {
        if (!invalidProps.includes(key)) {
            componentProps[key] = typeof value === 'function' && schema.value.bind
                ? value.bind(schema.value.bind)
                : value;
        }
    });

    if (prop.subtype) {
        componentProps.type = prop.subtype;
        delete componentProps.subtype;
    }

    if (!systemTypes.includes(type) && field) {
        componentProps.modelValue = Object.prototype.hasOwnProperty.call(prop, 'model')
            ? model
            : get(getFormModel(), field);
    }

    switch (type) {
        case 'form':
            delete componentProps.bind;
            delete componentProps.formItems;
            delete componentProps.colSpan;
            delete componentProps.gutter;
            return {
                ...setting.value.form,
                ...componentProps,
                model: model || getFormModel(),
            };
        case 'children':
            return {
                ...componentProps,
                type: rawType,
            };
        case 'item': {
            if (items) {
                delete componentProps.options;
                return {
                    ...setting.value.item,
                    ...componentProps,
                };
            }

            const {
                class: className,
                style,
                rules,
            } = prop;
            const classes = [className, rawType === 'button' ? 'sc-button' : '']
                .filter(Boolean)
                .join(' ');

            return {
                ...setting.value.item,
                label,
                style,
                rules,
                class: classes,
                prop: prop.prop || field,
            };
        }
        case 'button':
            return {
                ...setting.value.button,
                ...componentProps,
            };
        case 'select':
            delete componentProps.options;
            delete componentProps.props;
            return {
                ...setting.value.select,
                ...componentProps,
            };
        case 'input':
        case 'cascader':
        case 'radio':
        case 'radio-group':
        case 'checkbox':
        case 'checkbox-group': {
            delete componentProps.options;
            if (
                ['checkbox', 'checkbox-group'].includes(type)
                && typeof componentProps.modelValue === 'undefined'
            ) {
                componentProps.modelValue = [];
            }
            return {
                ...setting.value[type],
                ...componentProps,
            };
        }
        case 'upload':
            return {
                ...setting.value.upload,
                ...componentProps,
            };
        case 'title':
        case 'component':
            return {
                style: { margin: '0 ' + ((schema.value.gutter || 0) / 2) + 'px' },
                ...componentProps,
            };
        case 'dropdown':
            delete componentProps.menus;
            return {
                ...setting.value.dropdown,
                ...componentProps,
            };
        default:
            return componentProps;
    }
}

function updateModel(prop, value) {
    const modifier = getModifier(prop.type);
    let nextValue = value;

    if (modifier === 'trim' && typeof nextValue === 'string') {
        nextValue = nextValue.trim();
    } else if (modifier === 'number' && nextValue !== '' && !Number.isNaN(Number(nextValue))) {
        nextValue = Number(nextValue);
    }

    if (Object.prototype.hasOwnProperty.call(prop, 'model')) {
        if (!schema.value.bind) {
            console.error('Schema field "' + prop.field + '" requires a bind target.');
            return;
        }
        set(schema.value.bind, prop.field, nextValue);
        return;
    }

    const formModel = getFormModel();
    set(formModel, prop.field, nextValue);
    emit('update:modelValue', formModel);
}

function useEvent(prop = {}) {
    const { on = {}, field, type = '' } = prop;
    const listeners = {};

    Object.entries(on).forEach(([eventName, handler]) => {
        if (typeof handler !== 'function' || eventName.startsWith('keyup')) {
            return;
        }
        const normalizedName = eventName.replace(/\.native$/, '');
        listeners[normalizedName] = schema.value.bind
            ? handler.bind(schema.value.bind)
            : handler;
    });

    if (!field) {
        return listeners;
    }

    const modifier = getModifier(type);
    if (modifier === 'lazy') {
        const onChange = listeners.change;
        listeners.change = (value) => {
            updateModel(prop, value);
            onChange?.(value);
        };
    } else {
        const onUpdate = listeners['update:modelValue'];
        listeners['update:modelValue'] = (value) => {
            updateModel(prop, value);
            onUpdate?.(value);
        };
    }

    return listeners;
}

function useFn(fn, event) {
    if (!fn) {
        return;
    }
    const { bind } = schema.value;
    bind ? fn.call(bind, event) : fn(event);
}

function handleKeyup(item, event) {
    useFn(item.on?.keyup, event);
    useFn(item.on?.['keyup.native'], event);
    if (event.key === 'Enter') {
        useFn(item.on?.['keyup.enter'], event);
        useFn(item.on?.['keyup.enter.native'], event);
    }
}

function fixType(type) {
    switch (getType(type)) {
        case 'radio':
            return 'el-radio-group';
        case 'checkbox':
            return 'el-checkbox-group';
        default:
            return 'el-' + getType(type);
    }
}

function isElementControl(item) {
    return ELEMENT_CONTROL_TYPES.includes(getType(item.type));
}

function isType({ type = '' }, types) {
    return types.includes(getType(type));
}

function getForm() {
    return formInstance.value;
}

function getField(fieldName) {
    return instance.proxy.$refs[fieldName];
}

function reset(field) {
    const formModel = getFormModel();
    if (field) {
        set(formModel, field, cloneDeep(get(defaultValue, field)));
    } else {
        Object.keys(formModel).forEach((key) => {
            formModel[key] = Object.prototype.hasOwnProperty.call(defaultValue, key)
                ? cloneDeep(defaultValue[key])
                : undefined;
        });
    }
    emit('update:modelValue', formModel);
}

onMounted(() => {
    const bindTarget = schema.value.bind;
    if (bindTarget) {
        const fields = bindTarget.$fields || {};
        Object.assign(fields, instance.proxy.$refs);
        Reflect.set(bindTarget, '$fields', fields);
    }
});

defineExpose({
    elForm: formInstance,
    getForm,
    getField,
    reset,
});
</script>

<style scoped>
.inline {
    display: inline-block;
    width: auto;
    float: none;
}

.sc-form-title {
    line-height: 55px;
    font-weight: 700;
    font-size: 14px;
    vertical-align: top;
    clear: both;
}

.el-range-editor.el-input__wrapper {
    width: auto;
}

.sc-button.el-form-item {
    margin-bottom: 0;
}
</style>
